from django import template

register = template.Library()
@register.inclusion_tag('projekt/criterium.html')
def criterium_tag(criterium):
    subcriterias = criterium.children.all()
    return {'children': subcriterias}
