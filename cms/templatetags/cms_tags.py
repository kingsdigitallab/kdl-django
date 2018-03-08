from django import template
import random

register = template.Library()


@register.filter
def shuffle(arg):
    aux = list(arg)[:]
    random.shuffle(aux)
    return aux


@register.assignment_tag(takes_context=True)
def get_request_parameters(context, exclude=None):
    """Returns a string with all the request parameters except the exclude
    parameter."""
    params = ''
    request = context['request']

    for key, value in request.GET.items():
        if key != exclude:
            params += '&{key}={value}'.format(key=key, value=value)

    return params


@register.assignment_tag(takes_context=True)
def get_site_root(context):
    """Returns the site root Page, not the implementation-specific model used.
    Object-comparison to self will return false as objects would differ.

    :rtype: `wagtail.wagtailcore.models.Page`
    """
    return context['request'].site.root_page


@register.inclusion_tag('cms/tags/main_menu.html', takes_context=True)
def main_menu(context, root, current_page=None):
    """Returns the main menu items, the children of the root page. Only live
    pages that have the show_in_menus setting on are returned."""
    menu_pages = root.get_children().live().in_menu()

    root.active = (current_page.url == root.url
                   if current_page else False)

    for page in menu_pages:
        page.active = (current_page.url.startswith(page.url)
                       if current_page else False)

    return {'request': context['request'], 'root': root,
            'current_page': current_page, 'menu_pages': menu_pages}


@register.inclusion_tag('cms/tags/footer_menu.html', takes_context=True)
def footer_menu(context, root, current_page=None):
    """Returns the main menu items, the children of the root page. Only live
    pages that have the show_in_menus setting on are returned."""
    menu_pages = root.get_children().live().in_menu()

    root.active = (current_page.url == root.url
                   if current_page else False)

    for page in menu_pages:
        page.active = (current_page.url.startswith(page.url)
                       if current_page else False)

    return {'request': context['request'], 'root': root,
            'current_page': current_page, 'menu_pages': menu_pages}
