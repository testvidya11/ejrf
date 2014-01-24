from django import template

register = template.Library()

@register.filter
def display_list(_list):
    return ', '.join(_list)