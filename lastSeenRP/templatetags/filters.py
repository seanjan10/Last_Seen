from django import template
from django.template.defaultfilters import stringfilter


register = template.Library()

#filter to remove the whitespace from a value (most likely a last name) and replace it with underscores
@register.filter(name="remove_whitespace")
@stringfilter
def remove_whitespace(value):
    return value.replace(' ', '_')

#opposite of above
@register.filter(name="readd_whitespace")
@stringfilter
def readd_whitespace(value):
    return value.replace('_', ' ')
