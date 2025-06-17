from django import template
from django.urls import resolve, Resolver404
from ..models import Menu, MenuItem

register = template.Library()

@register.inclusion_tag('menu/menu.html', takes_context=True)
def draw_menu(context, menu_name):
    request = context['request']
    current_url = request.path_info
    
    try:
        menu = Menu.objects.prefetch_related('items').get(name=menu_name)
    except Menu.DoesNotExist:
        return {'menu': None}
    
    items = list(menu.items.all())
    menu_tree = build_menu_tree(items)
    
    active_item = None
    try:
        resolved_url = resolve(current_url)
        for item in items:
            if item.named_url and resolved_url.url_name == item.named_url:
                active_item = item
                break
            elif item.url and item.url == current_url:
                active_item = item
                break
    except Resolver404:
        pass
    
    expanded_items = set()
    if active_item:
        parent = active_item.parent
        while parent:
            expanded_items.add(parent.id)
            parent = parent.parent
        
        for child in active_item.children.all():
            expanded_items.add(child.id)
    
    return {
        'menu': menu,
        'menu_tree': menu_tree,
        'active_item': active_item,
        'expanded_items': expanded_items,
    }

def build_menu_tree(items, parent=None):
    result = []
    for item in items:
        if item.parent == parent:
            children = build_menu_tree(items, item)
            result.append({
                'item': item,
                'children': children,
                'has_children': bool(children),
            })
    return result   