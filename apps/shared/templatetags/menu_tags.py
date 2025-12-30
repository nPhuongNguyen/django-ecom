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
        return 'show'
    return ''

@register.simple_tag(takes_context=True)
def accordion_child(context, accordion_child):
    if context['accordion_child'] == accordion_child:
        return 'show'
    return ''

@register.simple_tag(takes_context=True)
def menu_item_show(context, menu_item_show):
    if context['menu_item_show'] == menu_item_show:
        return 'menu-item-show'
    return ''
