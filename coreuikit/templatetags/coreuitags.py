from django.template import Library, TemplateSyntaxError
from django.utils.safestring import mark_safe
from django.shortcuts import reverse
from coreuikit.utils.simpletag import SimpleTag  as T
from coreuikit.utils.helper import Helper

register = Library()
# punctuation remover


@register.filter
def render_table():
    pass


@register.filter
def render_tabs_content(contents, active_tab=None):
    html = []
    for name, content in contents.items():
        klass = 'tab-pane'
        if name == active_tab:
            klass += ' active'

        tab_name = 'tab_{}'.format(name)
        html.append(
            T.div(content, klass=klass, id=tab_name)
        )


    return mark_safe(''.join(html))


@register.filter
def render_tabs(tabs, active_tab=None):
    html = []

    if not active_tab:
        active_tab = Helper.convert_flat(tabs[0]['name'])

    for tab in tabs:
        #name = Helper.convert_flat(tab['name'])
        name = Helper.convert_flat( tab.get('alias', tab['name']) )
        tab_name = 'tab_{}'.format(name)
        #print(tab_name)
        tab_class_attr = 'nav-link'
        tab_class_attr += ' active' if name == active_tab else ''

        href = None

        if 'url' in tab:
            #print(tab)
            href = reverse(
                    tab['url'],
                    args=tab.get('url_args'),
                    kwargs=tab.get('url_kwargs'),
                    )
        elif 'link' in tab:
            href = tab['link']

        a_kwargs = {
            'klass': tab_class_attr,
            'href': href,
            'aria-controls': name
        }
        if not href:
            a_kwargs.update({
                'data-toggle': 'tab', 'role': 'tab',
                'href': '#{}'.format(tab_name)
            })

        a_content = '{}{}{}'.format(
            tab.get('pre_name', ''),
            tab['name'],
            tab.get('post_name', ''),
        )
        tab_link = T.a(a_content, **a_kwargs)
        html.append(T.li(tab_link, klass='nav-item'))

    tab_html = T.ul(''.join(html), klass='nav nav-tabs', role='tablist')
    return mark_safe(tab_html)

