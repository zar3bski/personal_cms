from django import template
register = template.Library()

@register.filter(name='range')
def filter_range(start, end):
  return range(start, end)

@register.filter
def multiply(value, arg, *args, **kwargs):
    return value * arg