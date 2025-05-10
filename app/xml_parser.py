import zipfile
import xml.etree.ElementTree as ET


class XmlParser:
    """
    Handles parsing of .pptx slide XML into structured content: text paragraphs and tables.
    Stores a mapping from slide index → parsed content.
    """
    def __init__(self, pptx_path):
        self.pptx_path = pptx_path
        self.namespace = {
            'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
            'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
            'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
        }
        self.slide_data = {}  # Maps slide index (0, 1, ...) → list of parsed shape info
        self.slide_links = {}
        self._parse_pptx()

    def _parse_pptx(self):
        """
        Parses the .pptx file and collects slides in the correct order by:
        1. Reading slide order from ppt/presentation.xml
        2. Mapping rIds to slide file names via ppt/_rels/presentation.xml.rels
        3. Ensuring the parsed slides match python-pptx order
        """
        with zipfile.ZipFile(self.pptx_path, 'r') as zipf:
            # Step 1: Read the presentation.xml to get rId order
            with zipf.open('ppt/presentation.xml') as pres_file:
                pres_root = ET.parse(pres_file).getroot()
                ns = {'p': 'http://schemas.openxmlformats.org/presentationml/2006/main'}
                sldIdLst = pres_root.find('p:sldIdLst', ns)
                rId_order = [sld.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id')
                             for sld in sldIdLst.findall('p:sldId', ns)]

            # Step 2: Read presentation.xml.rels to map rId to slide filenames
            with zipf.open('ppt/_rels/presentation.xml.rels') as rels_file:
                rels_root = ET.parse(rels_file).getroot()
                rId_to_target = {}
                for rel in rels_root:
                    rId = rel.attrib.get('Id')
                    target = rel.attrib.get('Target')
                    if rId and target and target.startswith("slides/slide"):
                        rId_to_target[rId] = target  # e.g., rId3 → slides/slide2.xml

            # Step 3: Map correct slide order
            ordered_slide_files = [f"ppt/{rId_to_target[rid]}" for rid in rId_order if rid in rId_to_target]

            # Step 4: Load hyperlinks from .rels files for each slide
            for idx, fname in enumerate(ordered_slide_files):
                rels_path = fname.replace("slides/", "slides/_rels/") + ".rels"
                links = {}
                try:
                    with zipf.open(rels_path) as rels_file:
                        rels_root = ET.parse(rels_file).getroot()
                        for rel in rels_root:
                            if rel.attrib.get("Type", "").endswith("/hyperlink"):
                                rId = rel.attrib["Id"]
                                target = rel.attrib["Target"]
                                links[rId] = target
                except KeyError:
                    raise RuntimeError("Error in Hyperlinks mapping\n")  # no .rels file for this slide
                self.slide_links[idx] = links
                """
                the above step builds a per-slide mapping like:
                self.slide_links[12] = {"rId2": "mailto:someone@example.com", "rId3": "https://google.com"}

                """

            # Step 5: Parse slides in correct order and store data
            for idx, fname in enumerate(ordered_slide_files):
                with zipf.open(fname) as file:
                    xml_content = file.read()
                    self.slide_data[idx] = self._parse_slide(xml_content,idx)


    def _parse_slide(self, xml_content, slide_index):
        """
        Parses a single slide and returns a list of shapes (paragraphs or tables) in order.
        """
        root = ET.fromstring(xml_content)
        ns = self.namespace
        shapes = []

        spTree = root.find('.//p:spTree', ns)
        for shape in spTree:
            tag = shape.tag.split("}")[-1]

            if tag == "sp":
                is_title = shape.find('.//p:nvPr/p:ph', ns) is not None and \
                           shape.find('.//p:nvPr/p:ph', ns).attrib.get('type') in ["title", "ctrTitle"]
                is_subtitle = shape.find('.//p:nvPr/p:ph', ns) is not None and \
                              shape.find('.//p:nvPr/p:ph', ns).attrib.get('type') == "subTitle"

                for paragraph in shape.findall('.//a:p', ns):
                    runs = []
                    for r in paragraph.findall('a:r', ns):
                        rpr = r.find('a:rPr', ns)
                        text_elem = r.find('a:t', ns)
                        if text_elem is None:
                            continue
                        text = text_elem.text or ""
                        bold = rpr is not None and rpr.attrib.get("b") == "1"
                        italic = rpr is not None and rpr.attrib.get("i") == "1"
                        underline = rpr is not None and rpr.attrib.get("u") in ["sng", "dbl"]
                        strike = rpr is not None and rpr.attrib.get("strike") in ["sng", "dbl"]

                        hlink = rpr.find('a:hlinkClick', ns)
                        r_id = hlink.attrib.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id') if hlink is not None else None
                        hyperlink = self.slide_links.get(slide_index, {}).get(r_id)

                        if hyperlink:
                            if hyperlink.startswith("mailto:"):
                                hyperlink_type = "email"
                            elif hyperlink.startswith("http://") or hyperlink.startswith("https://"):
                                hyperlink_type = "web"
                            else:
                                hyperlink_type = "other"
                        else:
                            hyperlink_type = None


                        runs.append({
                            "text": text,
                            "bold": bold,
                            "italic": italic,
                            "underline": underline,
                            "strikethrough": strike,
                            "hyperlink": hyperlink,
                            "hyperlink_type": hyperlink_type
                        })

                    # Reconstruct the plain string for logic/grouping
                    text = "".join(run["text"] for run in runs)
                    if not text.strip():
                        continue
                    # Get text alignment
                    alignment = 'left' # as PP default
                    pPr = paragraph.find('a:pPr',ns)
                    if pPr is not None and "algn" in pPr.attrib:
                        algn = pPr.attrib["algn"]
                        if algn == "ctr":
                            alignment = "center"
                        elif algn == "r":
                            alignment = "right"

                    bullet_type = None if is_title or is_subtitle else self._get_bullet_type(paragraph)
                    level = self._get_level(paragraph, bullet_type)

                    shapes.append({
                        "text": text.strip(),
                        "runs": runs,
                        "level": level,
                        "bullet_type": bullet_type,
                        "title": is_title,
                        "type": "text",
                        "alignment": alignment
                    })

            # table data extract
            elif tag == "graphicFrame":
                tbl = shape.find('.//a:tbl', ns)
                if tbl is not None:
                    rows = []
                    for tr in tbl.findall('.//a:tr', ns):
                        row = []
                        for tc in tr.findall('.//a:tc', ns):
                            texts = [t.text for t in tc.findall('.//a:t', ns) if t.text]
                            cell = " ".join(texts).strip()
                            row.append(cell)
                        rows.append(row)


                    # Extract the shape transform (position and size) if available
                    xfrm = shape.find('.//p:xfrm', ns)
                    if xfrm is not None:
                        off = xfrm.find('a:off', ns)
                        ext = xfrm.find('a:ext', ns)
                        try:
                            x = int(off.attrib["x"]) if off is not None else 0
                            y = int(off.attrib["y"]) if off is not None else 0
                            cx = int(ext.attrib["cx"]) if ext is not None else 0
                            cy = int(ext.attrib["cy"]) if ext is not None else 0
                        except Exception as e:
                            print("⚠️ Failed to extract table position:", e)
                            x = y = cx = cy = 0
                    else:
                        print("⚠️ Missing <a:xfrm> for table shape")
                        x = y = cx = cy = 0

                    # Convert to percentages based on slide size (in EMUs)
                    # PowerPoint default size = 9144000 x 6858000 EMUs = 960 x 720 pixels
                    # PowerPoint uses EMUs (English Metric Units)
                    # 1 inch = 914400 EMUs → slide width = 10" = 9144000 EMUs
                    # 1 pixel ≈ 9525 EMUs, but we work in % relative to slide
                    # This makes the Reveal layout scale properly on all screens

                    SLIDE_WIDTH_EMU = 9144000
                    SLIDE_HEIGHT_EMU = 6858000

                    x_percent = (x / SLIDE_WIDTH_EMU) * 100
                    y_percent = (y / SLIDE_HEIGHT_EMU) * 100
                    width_percent = (cx / SLIDE_WIDTH_EMU) * 100
                    height_percent = (cy / SLIDE_HEIGHT_EMU) * 100


                    # Extract column widths from <a:tblGrid>
                    col_widths = []
                    tbl_grid = tbl.find('a:tblGrid', ns)
                    if tbl_grid is not None:
                        for grid_col in tbl_grid.findall('a:gridCol', ns):
                            w_emu = int(grid_col.attrib.get("w", "0"))
                            width_percent = (w_emu / SLIDE_WIDTH_EMU) * 100
                            col_widths.append(width_percent)


                    # Add all data to the table shape dict
                    shapes.append({
                        "type": "table",
                        "rows": rows,
                        "x_percent": x_percent,
                        "y_percent": y_percent,
                        "width_percent": width_percent,
                        "height_percent": height_percent,
                        "col_widths": col_widths
                    })

        return shapes


    def _get_bullet_type(self, paragraph):
        """
        Determines whether the <a:p> paragraph should be treated as:
        - "bullet" (unordered list)
        - "number" (ordered list)
        - None (normal paragraph)

        Logic:
        - If <a:buNone> is present anywhere → this paragraph is NOT a bullet.
        - If <a:buAutoNum> is present → this is a numbered list.
        - If <a:buChar> is present → this is a bullet list.
        - If none of the above, and no buNone, we assume it's a bullet (usually level 0).
        """
        ns = self.namespace

        # ✅ Look for tags directly inside <a:p>, not just <a:pPr>
        buNone = paragraph.find('.//a:buNone', ns)
        buChar = paragraph.find('.//a:buChar', ns)
        buAutoNum = paragraph.find('.//a:buAutoNum', ns)

        # 🔍 Case 1: <a:buNone> — explicitly says it's a normal paragraph
        if buNone is not None:
            return None

        # 🔢 Case 2: <a:buAutoNum> — indicates numbered list (1., 2., ...)
        if buAutoNum is not None:
            return "number"

        # • Case 3: <a:buChar> — indicates bulleted list (•, →, etc.)
        if buChar is not None:
            return "bullet"

        # 🟡 Case 4: No explicit tags, but also no <a:buNone>
        #           Treat as default top-level bullet 
        return "bullet"

    def _get_level(self, paragraph, bullet_type):
        """
        Extracts bullet indentation level from <a:pPr>. Defaults to 0.
        """
        ns = self.namespace
        pPr = paragraph.find('a:pPr', ns)
        if pPr is not None and 'lvl' in pPr.attrib:
            return int(pPr.attrib['lvl'])
        if bullet_type in ("bullet", "number"):
            return 0  # Default to level 0 if it's bullet but no lvl tag
        return 0


    def get_slide_shapes(self, slide_index):
        """
        Returns the list of parsed shapes for a given slide index.
        Each shape is a dict of either:
        - type="text", with keys: text, level, bullet_type, title
        - type="table", with key: rows (list of lists)
        """
        return self.slide_data.get(slide_index, [])