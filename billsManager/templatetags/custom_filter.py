from django import template

register = template.Library()

@register.filter(name='instanceof')
def instanceof(value, arg):
    return isinstance(value, arg)
