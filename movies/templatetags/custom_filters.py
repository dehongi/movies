from django import template

register = template.Library()


@register.filter
def floordiv(value, arg):
    try:
        return value // arg
    except (ValueError, TypeError):
        return 0


@register.filter
def mul(value, arg):
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0
