from django import template

register = template.Library()


@register.filter()
def media_filter(path: str | None) -> str:
    if path:
        return f"media/{path}"
    return "#"
