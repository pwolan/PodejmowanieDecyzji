from django import template

register = template.Library()

@register.filter(name='lookup')
def lookup(value, arg):
    return value[arg]

@register.filter(name='concat')
def concat(str1, str2):
    return str(str1) + str(str2)

@register.filter(name='make_id')
def make_id(id1, id2):
    return f"_{id1}-{id2}"