import os
from .slide import (
    HTMLSlide, TitleShape,TextShape, 
    ParagraphContent, BulletTreeContent, BulletNode, 
    TableContent, ImageContent 
)
from .pptx_parser import PptxParser


class SlideConverter:

    def __init__(self, pptx_path):
        self.pptx_path = pptx_path
        self.slides = []

    def convert(self): 
        parser = PptxParser(self.pptx_path)
        for i in range(parser.get_slide_count()):
            slide_shapes = parser.get_slide_shapes(i)
            slide = self.convert_slide(slide_shapes)
            self.slides.append(slide)
       

    def convert_slide(self, shapes_data):
        """
        Given pre-parsed shapes metadata from XML, group and convert content
        into Reveal.js-compatible HTML slide structure.
        """
        title_shapes = []
        contents = []

        for shape in shapes_data:
            
            
            if shape["type"] == "table":
                contents.append(TableContent(shape))
                continue
            
            if shape["type"] == "image":
                contents.append(ImageContent(shape))
                continue

            if shape["title"] in ("title", "ctrTitle", "subTitle"):
                para = next((c for c in shape["contents"] if c["type"] == "paragraph"), None)
                if para:
                    title_shapes.append(TitleShape(shape, para["runs"], para.get("alignment")))
                continue

            elif shape["type"] == "text" and shape["title"] is None:

                buffer = []
                last_type = None
                textShape_content = []

                def flush():
                    nonlocal buffer, last_type
                    if not buffer:
                        return
                    if last_type in ("bullet", "numbered"):
                        ordered = (last_type == "numbered")
                        root = BulletNode("ROOT", -1, ordered)
                        stack = [root]
                        for item in buffer:
                            node = BulletNode(item["runs"], item["level"], ordered, item["alignment"])
                            while stack and stack[-1].level >= node.level:
                                stack.pop()
                            stack[-1].add_child(node)
                            stack.append(node)
                        textShape_content.append(BulletTreeContent(root))
                    elif last_type == "paragraph":
                        for item in buffer:
                            textShape_content.append(ParagraphContent(item["runs"], item["alignment"]))
                    buffer.clear()
                    last_type = None

                for block in shape["contents"]:
                    if block["type"] not in ("paragraph", "bullet"):
                        continue

                    bullet_type = block.get("bullet_type")
                    current_type = (
                        "numbered" if bullet_type == "number"
                        else "bullet" if bullet_type == "bullet"
                        else "paragraph"
                    )

                    if last_type is None or last_type == current_type:
                        buffer.append(block)
                        last_type = current_type
                    else:
                        flush()
                        buffer = [block]
                        last_type = current_type

                flush()

                # textshape_content is a list of parag. and lists objects
                contents.append(TextShape(shape, textShape_content))


        slide = HTMLSlide(title_shapes, transition="fade")
        for shape in contents:
            slide.add_shape(shape)

        
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
