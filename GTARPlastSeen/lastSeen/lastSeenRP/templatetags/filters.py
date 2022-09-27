from django import template
from django.template.defaultfilters import stringfilter


register = template.Library()

#could adjust to be any value instead of just space
@register.filter(name="remove_whitespace")
@stringfilter
def remove_whitespace(value):
    return value.replace(' ', '_')


@register.filter(name="readd_whitespace")
@stringfilter
def readd_whitespace(value):
    return value.replace('_', ' ')
