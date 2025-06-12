from abc import ABC, abstractmethod

class SlideContent(ABC):
    """
    Abstract base class for all content blocks on a slide.
    Each subclass must implement the to_html method.
    """
    @abstractmethod
    def to_html(self):
        pass


class HTMLSlide:
    """
    Represents one full Reveal.js slide.
    Contains a title and ordered list of content blocks.
    """
    def __init__(self, title_shapes=None, transition="fade"):
        self.title_shapes = title_shapes or None
        self.transition = transition
        self.shapes = []

    def add_shape(self, shape):
        self.shapes.append(shape)

    def to_html(self):
        html = f'''<section style="position: relative;" data-transition="{self.transition}" 
                    width:100%; height:100%;>\n'''

        if self.title_shapes:
            for title in self.title_shapes:
                html += title.to_html()

        for shape in self.shapes:
            html += shape.to_html()

        html += "</section>\n"
        return html


class ParagraphContent(SlideContent):
    """
    Represents a plain paragraph block.
    """
    def __init__(self, runs, alignment="left"):
        self.runs = runs
        self.alignment = alignment

    def to_html(self):
        html = f"  <p class='fragment' style='text-align:{self.alignment};'>\n"
        for run in self.runs:
            text = run["text"]

            # # Apply tag-based styling for bold/italic/underline
            if run.get("bold"):
                text = f"<strong>{text}</strong>"
            if run.get("italic"):
                text = f"<em>{text}</em>"
            if run.get("underline"):
                text = f"<u>{text}</u>"

            # Build the CSS style string for this run
            style = ""
            if run.get("font_size_px"):
                style += f"font-size:{run['font_size_px']:.2f}px;"
            if run.get("strikethrough"):
                style += "text-decoration: line-through;"
            # Wrap in a span for style (only if style string is not empty)
            if style:
                text = f"<span style='{style}'>{text}</span>"

            # Wrap with link if hyperlink is present (is always outmost)
            if run.get("hyperlink"):
                url = run["hyperlink"]
                text = f"<a href='{url}' target='_blank'>{text}</a>"

            html += text + "\n"
        html += "  </p>\n"
        return html


class BulletNode(SlideContent):
    """
    Represents a bullet point.
    """
    def __init__(self, runs, level, ordered=False, alignment="left"):
        self.runs = runs
        self.level = level
        self.ordered = ordered
        self.children = []
        self.alignment = alignment

    def add_child(self, node):
        self.children.append(node)

    def to_html(self):
        html = f"<li class='fragment' style='text-align:{self.alignment};'>\n"
        for run in self.runs:
            text = run["text"]
            # # Apply tag-based styling for bold/italic/underline
            if run.get("bold"):
                text = f"<strong>{text}</strong>"
            if run.get("italic"):
                text = f"<em>{text}</em>"
            if run.get("underline"):
                text = f"<u>{text}</u>"

            # Build the CSS style string for this run
            style = ""
            if run.get("font_size_px"):
                style += f"font-size:{run['font_size_px']:.2f}px;"
            if run.get("strikethrough"):
                style += "text-decoration: line-through;"
            # Wrap in a span for style (only if style string is not empty)
            if style:
                text = f"<span style='{style}'>{text}</span>"

            # Wrap with link if hyperlink is present
            if run.get("hyperlink"):
                url = run["hyperlink"]
                text = f"<a href='{url}' target='_blank'>{text}</a>"

            html += text

        if self.children:
            tag = "ol" if self.ordered else "ul"
            html += f"<{tag}>\n"
            for child in self.children:
                html += child.to_html() 
            html += f"</{tag}>\n"
        html += "\n</li>\n"
        return html


class BulletTreeContent(SlideContent):
    def __init__(self, root):
        self.root = root  # root: a BulletNode with ordered flag

    def to_html(self):
        tag = "ol" if self.root.ordered else "ul"
        html = f"<{tag}>\n"
        for node in self.root.children:
            html += node.to_html() 
        html += f"</{tag}>"
        return html

class TableContent(SlideContent):
    """
    Represents a table block, including its layout on the slide.
    x/y: Top-left corner (in % of slide width/height)
    width/height: Size of the table (in % of slide width/height)
    """
    def __init__(self, shape_dict):
        self.rows = shape_dict["rows"]  # List of rows, each row is a list of cell texts
        self.x_percent = shape_dict["x_percent"]
        self.y_percent = shape_dict["y_percent"]
        self.width_percent = shape_dict["width_percent"]
        self.height_percent = shape_dict["height_percent"]
        self.col_widths = shape_dict["col_widths"] or []

        
    def to_html(self):

        top = self.y_percent
        left = self.x_percent
        width = self.width_percent
        height = self.height_percent
        # Create absolute-positioned container using percentages
        style = ""
        if all(v is not None for v in [self.x_percent, self.y_percent, self.width_percent, self.height_percent]):
            style = (
                f"position:absolute;"
                f" top:{top:.2f}%;"
                f" left:{left:.2f}%;"
                f" width:{width:.2f}%;"
                f" height:{height:.2f}%;"
            )
        ##############
        #<div style="overflow-x: auto; overflow-y: auto; max-height: 100%;">
        """html = f'''
        <div style="{style} "\n>

        ''' """
        #############
        html = f'<div style="{style}">\n'

        html += '<table class="fragment auto-fit">\n'

        # Insert colgroup if column widths are available
        if self.col_widths:
            html += "  <colgroup>\n"
            for col_width in self.col_widths:
                html += f'    <col style="width:{col_width:.2f}%;">\n'
            html += "  </colgroup>\n"

        for i, row in enumerate(self.rows):
            tag = "th" if i == 0 else "td"
            html += "<tr>"
            for cell_runs in row:
                html += f"<{tag}>"
                for run in cell_runs:
                    text = run["text"]
                    # # Apply tag-based styling for bold/italic/underline
                    if run.get("bold"):
                        text = f"<strong>{text}</strong>"
                    if run.get("italic"):
                        text = f"<em>{text}</em>"
                    if run.get("underline"):
                        text = f"<u>{text}</u>"

                    # Build the CSS style string for this run
                    style = ""
                    if run.get("font_size_px"):
                        style += f"font-size:{run['font_size_px']:.2f}px;"
                    if run.get("strikethrough"):
                        style += "text-decoration: line-through;"
                    # Wrap in a span for style (only if style string is not empty)
                    if style:
                        text = f"<span style='{style}'>{text}</span>"

                    # Wrap with link if hyperlink is present
                    if run.get("hyperlink"):
                        url = run["hyperlink"]
                        text = f"<a href='{url}' target='_blank'>{text}</a>"
                    html += text
                html += f"</{tag}>"
            html += "</tr>\n"
        html += "</table></div>\n"
        return html


class TextShape(SlideContent):
    def __init__(self, shape_dict, contents):
        
        self.x_percent = shape_dict["x_percent"]
        self.y_percent = shape_dict["y_percent"]
        self.width_percent = shape_dict["width_percent"]
        self.height_percent = shape_dict["height_percent"]
        self.contents = contents  # list of ParagraphContent / BulletTreeContent

    def to_html(self):

        top = max(self.y_percent, 0)
        left = max(self.x_percent, 0)
        width = min(self.width_percent, 100)
        height = min(self.height_percent, 100)
        style = (
            f"position:absolute;"
            f" top:{top:.2f}%;"
            f" left:{left:.2f}%;"
            f" width:{width:.2f}%;"
            f" height:{height:.2f}%;"
        )

        # Outer container layout
        html = f'<div class="text-shape" style="{style} font-size:30px;">\n'

        for content in self.contents:
            html += content.to_html()

        html += '</div>\n'
        return html



class TitleShape(SlideContent):
    def __init__(self, shape_dict, title_runs, align):
        
        self.x_percent = shape_dict["x_percent"]
        self.y_percent = shape_dict["y_percent"]
        self.width_percent = shape_dict["width_percent"]
        self.height_percent = shape_dict["height_percent"]
        self.title_type = shape_dict.get("title", None)  # 'ctrTitle', 'title', 'subTitle'
        self.content = title_runs 
        self.alignment = align

    def to_html(self):
        top = max(self.y_percent, 0)
        left = max(self.x_percent, 0)
        width = min(self.width_percent, 100)
        height = min(self.height_percent, 100)
        style = (
            f"position:absolute;"
            f" top:{top:.2f}%;"
            f" left:{left:.2f}%;"
            f" width:{width:.2f}%;"
            f" height:{height:.2f}%;"
        )

        title = self.title_type
        tag = "h3" if title in ("ctrTitle", "title") else "h4"
        align = self.alignment

        html = f'<div class="title-shape fit-content" style="{style}">\n'
        html += f'<{tag} style="text-align:{align}; max-height:{height:.2f}%;" class="fit-text">'

        for run in self.content:
            text = run["text"]
            # # Apply tag-based styling for bold/italic/underline
            if run.get("bold"):
                text = f"<strong>{text}</strong>"
            if run.get("italic"):
                text = f"<em>{text}</em>"
            if run.get("underline"):
                text = f"<u>{text}</u>"

            # Build the CSS style string for this run
            style = ""
            if run.get("font_size_px"):
                style += f"font-size:{run['font_size_px']:.2f}px;"
            if run.get("strikethrough"):
                style += "text-decoration: line-through;"
            # Wrap in a span for style (only if style string is not empty)
            if style:
                text = f"<span style='{style}'>{text}</span>"

            # Wrap with link if hyperlink is present
            if run.get("hyperlink"):
                url = run["hyperlink"]
                text = f"<a href='{url}' target='_blank'>{text}</a>"

            html += text

        html += f"</{tag}>\n</div>\n"
        return html



class ImageContent(SlideContent): 
    """
    Represents an image block, absolutely positioned, with size as percent of slide.
    """
    def __init__(self, shape_dict):
        self.x_percent = shape_dict["x_percent"]
        self.y_percent = shape_dict["y_percent"]
        self.width_percent = shape_dict["width_percent"]
        self.height_percent = shape_dict["height_percent"]
        self.image_path = shape_dict["image_path"]
        self.alt = shape_dict.get("alt", "Slide Image")

    def to_html(self):
        # Compose the style for the div container
        style = (
            f"position:absolute;"
            f" top:{self.y_percent:.2f}%;"
            f" left:{self.x_percent:.2f}%;"
            f" width:{self.width_percent:.2f}%;"
            f" height:{self.height_percent:.2f}%;"
        )
        # Image path is already relative (e.g., "images/slide1_img1.png")
        html = (
            f'<div class="image-shape" style="{style}">\n'
            f'  <img src="{self.image_path}" '
            f'style="width:100%; height:100%; object-fit:contain;" alt="{self.alt}">\n'
            f'</div>\n'
        )
        return html

