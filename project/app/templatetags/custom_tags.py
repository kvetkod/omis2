from django import template

register = template.Library()


@register.filter
def dict_get(dict_data, key):
    return dict_data.get(key)


@register.filter
def attr(obj, attr_name):
    return getattr(obj, attr_name)
