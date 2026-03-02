from django import template
import re

register = template.Library()

@register.filter(is_safe=True)
def highlight(text, query):
    if not query:
        return text
    pattern = re.compile(re.escape(query), re.IGNORECASE)
    return pattern.sub(lambda m: f'<span style="background-color:#007399">{m.group(0)}</span>', text)