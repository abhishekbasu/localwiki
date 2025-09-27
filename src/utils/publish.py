from markdown import markdown


def render_markdown(mdtext: str, title: str) -> str:
    """Convert markdown text to HTML"""
    mdtext = f"#{title.capitalize()}" + "\n" + mdtext
    html_output = markdown(mdtext)
    return html_output
