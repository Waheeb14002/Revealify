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
    def __init__(self, title="", transition="fade"):
        self.title = title
        self.transition = transition
        self.contents = []

    def add_content(self, content):
        self.contents.append(content)

    def to_html(self):
        html = f"<section data-transition='{self.transition}'>\n"

        # Detect if table exists in this slide's contents so we make title bit smaller
        has_table = any(isinstance(content, TableContent) for content in self.contents)

        # Detect if any non-table text exists
        has_non_table = any(not isinstance(content, TableContent) for content in self.contents)

        # Start r-fit-text div only for text content
        # ensures to fit bit larger slides, anyways its not common to make extra large pp slides
        if has_non_table:
            html += '<div class="r-fit-text">\n'

        if self.title:
            # If table exists, make title smaller automatically (use h3 or h4)
            title_tag = "h4" if has_table else "h2"
            html += f"  <{title_tag}>{self.title}</{title_tag}>\n"

        # Handle contents differently, cus we put scroller for tables
        for content in self.contents:
            if isinstance(content, TableContent):
                if has_non_table:
                    # Close fit-text div BEFORE table
                    html += '</div>\n'  

                html += content.to_html() + "\n"

                if has_non_table:
                    # Reopen fit-text div AFTER table (if we expect more text below)
                    html += '<div class="r-fit-text">\n'
            else:
                html += content.to_html() + "\n"
        if has_non_table:
            html += '</div>\n'  # Final closing of r-fit-text
        html += "</section>\n"
        return html


class ParagraphContent(SlideContent):
    """
    Represents a plain paragraph block.
    """
    def __init__(self, runs):
        self.runs = runs

    def to_html(self):
        html = "  <p class='fragment'>"
        for run in self.runs:
            text = run["text"]
            if run.get("bold"):
                text = f"<strong>{text}</strong>"
            if run.get("italic"):
                text = f"<em>{text}</em>"
            if run.get("underline"):
                text = f"<u>{text}</u>"
            if run.get("strikethrough"):
                text = f"<span style='text-decoration: line-through;'>{text}</span>"
            html += text
        html += "</p>"
        return html


class BulletNode(SlideContent):
    """
    Represents a bullet point.
    """
    def __init__(self, runs, level, ordered=False):
        self.runs = runs
        self.level = level
        self.ordered = ordered
        self.children = []

    def add_child(self, node):
        self.children.append(node)

    def to_html(self):
        html = "<li class='fragment'>"
        for run in self.runs:
            text = run["text"]
            if run.get("bold"):
                text = f"<strong>{text}</strong>"
            if run.get("italic"):
                text = f"<em>{text}</em>"
            if run.get("underline"):
                text = f"<u>{text}</u>"
            if run.get("strikethrough"):
                text = f"<span style='text-decoration: line-through;'>{text}</span>"
            html += text
            
        if self.children:
            tag = "ol" if self.ordered else "ul"
            html += f"<{tag}>"
            for child in self.children:
                html += child.to_html()
            html += f"</{tag}>"
        html += "</li>"
        return html


class BulletTreeContent(SlideContent):
    def __init__(self, root):
        self.root = root  # root: a BulletNode with ordered flag

    def to_html(self):
        tag = "ol" if self.root.ordered else "ul"
        html = f"<{tag}>"
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
    def __init__(self, rows, x_percent=None, y_percent=None, width_percent=None, height_percent=None,col_widths=None):
        self.rows = rows  # List of rows, each row is a list of cell texts
        self.x_percent = x_percent
        self.y_percent = y_percent
        self.width_percent = width_percent
        self.height_percent = height_percent
        self.col_widths = col_widths or []

        
    def to_html(self):
        # Create absolute-positioned container using percentages
        style = ""
        if all(v is not None for v in [self.x_percent, self.y_percent, self.width_percent, self.height_percent]):
            style = (
                f"position:absolute;"
                f" top:{self.y_percent:.2f}%;"
                f" left:{self.x_percent:.2f}%;"
                f" width:{self.width_percent:.2f}%;"
                f" height:{self.height_percent:.2f}%;"
            )
        #<div style="overflow-x: auto; overflow-y: auto; max-height: 100%;">
        html = f'''
        <div style="{style}; ">

        '''
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
            for cell in row:
                html += f"<{tag}>{cell}</{tag}> "
            html += "</tr>\n"
        html += "</table></div>\n"
        return html
