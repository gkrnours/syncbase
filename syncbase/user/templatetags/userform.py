from django import template

register = template.Library()

@register.filter
def field(form, field):
    return form[field]
