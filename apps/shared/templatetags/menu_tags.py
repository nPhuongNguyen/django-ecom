from django import template
register = template.Library()

@register.simple_tag(takes_context=True)
def active_space(context, space_current):
    if context['space_code'] == space_current:
        return 'active'
    return ''

@register.simple_tag(takes_context=True)
def accordion(context, accordion):
    if context['accordion'] == accordion:
        return 'here show kt-menu-item-accordion'
    return ''