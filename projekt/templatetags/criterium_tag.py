from django import template

register = template.Library()
@register.inclusion_tag('projekt/criterium.html')
def criterium_tag(criterium, to_delete=False, scenario_id=None):
    subcriterias = criterium.children.all()
    return {'children': subcriterias, 'to_delete': to_delete, 'scenario_id': scenario_id}


