from django import template

register = template.Library()

@register.filter
def get_form(question, formsets):
    return formsets.next_ordered_form(question).visible_fields()[0]