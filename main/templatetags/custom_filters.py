# Создаем новый фильтр в файле templatetags/custom_filters.py

from django import template

register = template.Library()


@register.filter(name="get_value_by_key")
def get_value_by_key(dictionary, key):
    return dictionary.get(key, 0)
