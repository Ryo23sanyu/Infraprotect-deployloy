from django import template

register = template.Library()

@register.filter
def split_comma(value):
    # valueがNoneの場合、空のリストを返す
    if not value:
        return []
    return value.split(",")