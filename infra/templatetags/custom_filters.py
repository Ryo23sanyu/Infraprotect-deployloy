import re
from django import template

register = template.Library()

@register.filter
def split_comma(value):
    # valueがNoneの場合、空のリストを返す
    if not value:
        return []
    return value.split(",")

@register.filter(name='store')
def store(value, storage):
    if 'value' not in storage:
        storage['value'] = value
        return None
    previous = storage['value']
    storage['value'] = value
    return previous