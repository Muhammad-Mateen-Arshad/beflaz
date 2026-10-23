import json
import re
from xml.sax.saxutils import escape

def esc(text):
    """Escape text for HTML."""
    return escape(text or "")

def html_to_text(html):
    """Strip HTML tags from a string."""
    if not html:
        return ""
    text = re.sub(r'<[^>]+>', ' ', html)
    return ' '.join(text.split())

def shorten(text, max_length):
    """Shorten text to max_length with an ellipsis."""
    if not text:
        return ""
    text = str(text)
    if len(text) <= max_length:
        return text
    return text[:max_length - 3].rsplit(' ', 1)[0] + '...'

def json_str(text):
    """Safely escape text for JSON/Schema markup values."""
    if not text:
        return ""
    # json.dumps adds double quotes around the string, e.g., "text"
    # [1:-1] removes these outer quotes so it fits safely inside your template quotes
    return json.dumps(str(text))[1:-1]
