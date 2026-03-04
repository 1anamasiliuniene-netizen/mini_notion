from django import template
import re
from django.utils.html import escape
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def highlight(text, query):
    text = text or ""
    if not query:
        return escape(text)

    pattern = re.compile(re.escape(query), re.IGNORECASE)
    parts = []
    last_end = 0

    for match in pattern.finditer(text):
        parts.append(escape(text[last_end:match.start()]))
        parts.append(f'<span style="background-color:#007399">{escape(match.group(0))}</span>')
        last_end = match.end()

    parts.append(escape(text[last_end:]))
    return mark_safe("".join(parts))
