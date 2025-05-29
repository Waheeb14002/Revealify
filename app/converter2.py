import os
from .slide import HTMLSlide, ParagraphContent, BulletNode, BulletTreeContent, TableContent
from .xml_parser import XmlParser


class SlideConverter:
    """
    Converts a PowerPoint (.pptx) file into Reveal.js-compatible slides.
    Uses only raw XML parsing for full control over structure and styling.
    """

    def __init__(self, pptx_path):
        self.pptx_path = pptx_path
        self.slides = []

    def convert(self):
        # Initialize XML parser and extract slide shapes
        try:
            xml_parser = XmlParser(self.pptx_path)
        except Exception as e:
            raise RuntimeError(f"Failed to initialize XML parser: {e}")

        # Loop over slides using correct XML order
        slide_count = xml_parser.get_slide_count()
        for i in range(slide_count):
            # Get structured shape data for slide i
            try:
                shapes = xml_parser.get_slide_shapes(i)
            except Exception as e:
                raise RuntimeError(f"Failed to extract shapes from slide {i}: {e}")

            # Convert extracted data to Reveal.js HTML slide
            try:
                slide = self.convert_slide(shapes)
            except Exception as e:
                raise RuntimeError(f"Failed to convert slide {i}: {e}")

            self.slides.append(slide)

    def convert_slide(self, shapes_data):
        """
        Given pre-parsed shapes metadata from XML, group and convert content
        into Reveal.js-compatible HTML slide structure.
        """

        title_runs = ""
        contents = []

        # If first shape is a title, extract and remove it
        if shapes_data and shapes_data[0].get("title", False):
            title_runs = shapes_data[0]["runs"]
            shapes_data = shapes_data[1:]

        buffer = []
        last_type = None

        # Group and convert content with buffer + flush method
        def flush_buffer():
            """
            Converts accumulated text items (paragraphs/bullets) into structured content blocks.
            """
            nonlocal buffer, last_type
            if not buffer:
                return

            if last_type in ("bullet", "numbered"):
                ordered = (last_type == "numbered")
                root = BulletNode("ROOT", -1, ordered)  # Dummy root to hold top level bullets and nested levels
                stack = [root]
                for item in buffer:
                    node = BulletNode(item["runs"], item["level"], ordered, item["alignment"])
                    while stack and stack[-1].level >= node.level:
                        stack.pop()
                    stack[-1].add_child(node)
                    stack.append(node)
                contents.append(BulletTreeContent(root))

            elif last_type == "paragraph":
                for item in buffer:
                    contents.append(ParagraphContent(item["runs"], item["alignment"]))

            buffer.clear()

        # Process each shape in this slide
        for item in shapes_data:

            # Handle table blocks directly
            if item["type"] == "table":
                flush_buffer() # flush pending bullets/paragraphs first
                contents.append(TableContent(
                    rows=item["rows"],
                    x_percent=item.get("x_percent"),
                    y_percent=item.get("y_percent"),
                    width_percent=item.get("width_percent"),
                    height_percent=item.get("height_percent"),
                    col_widths=item.get("col_widths")
                ))
                last_type = None   # reset buffer trackin
                continue  # skip rest of this loop

            # Handle textual content (paragraphs or bullets)
            elif item["type"] == "text":
                bullet_type = item["bullet_type"]

                # Determine paragraph type
                if bullet_type == "number":
                    current_type = "numbered"
                elif bullet_type == "bullet":
                    current_type = "bullet"
                else:
                    current_type = "paragraph"

                entry = {
                    "text": item["text"],
                    "runs": item.get("runs", []),
                    "level": item["level"],
                    "alignment": item.get("alignment", "left")
                }

                if last_type is None or current_type == last_type:
                    buffer.append(entry)
                else:
                    flush_buffer()
                    buffer = [entry]

                last_type = current_type

            else:
                # 🔧 unsupported types yet to come
                pass

        flush_buffer()  # Final flush after all shapes are processed

        #  Construct slide and append converted content
        slide = HTMLSlide(title_runs=title_runs, transition="fade")
        for content in contents:
            slide.add_content(content)

        return slide

    def save(self, output_file="slides.html"):
        """
        Write all converted slides into a Reveal.js-compatible HTML file.
        """
        try:
            os.makedirs("static", exist_ok=True)
            output_path = os.path.join("static", output_file)
            with open(output_path, "w", encoding="utf-8") as f:
                for slide in self.slides:
                    f.write(slide.to_html())
        except Exception as e:
            raise RuntimeError(f"Failed to write HTML to slides.html: {e}")
