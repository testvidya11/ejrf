from django import template

register = template.Library()

@register.filter
def get_form(question, ordered_forms):
    print question
    print question in ordered_forms.keys()
    print ordered_forms
    return ordered_forms[question]