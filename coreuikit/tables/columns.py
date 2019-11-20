import django_tables2 as tables
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from django.urls import reverse
from ..utils.simpletag import SimpleTag as T


class SequenceNumberColumn(tables.Column):
    empty_values = ()
    verbose_name = '#'
    orderable = False


class ListingColumn(tables.Column):
    max_count = None
    blank_val = None

    def __init__(self, max_count=None, blank_val='---', *args, **kwargs):
        self.max_count = max_count
        self.blank_val = blank_val
        tables.Column.__init__(self, *args, **kwargs)

    def render(self, value):
        if not value:
            return self.blank_val

        count = value.count()
        if count == 0:
            return self.blank_valt
        counter = 0
        is_exceed = False
        pack = []
        for v in value.all():
            counter += 1
            pack.append('<li>{}</li>'.format(v))
            if self.max_count and counter >= self.max_count:
                is_exceed = True
                pack.append('<li>...</li>')
                break
        html = '<ul>{}</ul>'.format(''.join(pack))

        if is_exceed:
            html += '<span class="badge badge-primary">{} remaining</span>'.format(
                count - counter
            )
        return mark_safe(html)


class ActionColumn(tables.Column):
    """
    table's column action, default to view, update and delete
    """
    # TODO: cari tahu cara set header gimana ?
    # TODO: translation
    empty_values = ()

    actions = ()
    record = None

    def __init__(self, actions=('view', 'update', 'delete'), *args, **kwargs):
        self.actions = actions
        return super().__init__(*args, **kwargs)

    @property
    def url_name(self) -> str:
        """
        Parent untuk actuan penanaam url depan
        :return:
        """
        return '{}_'.format(self.record._meta.model_name)

    def get_links_kwargs(self):
        return {'pk': self.record.pk}

    def get_link_view_kwargs(self):
        return self.get_links_kwargs()

    def get_link_view(self):
        return {
            'name': 'View',
            'href': reverse('{}detail'.format(self.url_name), kwargs=self.get_link_view_kwargs()),
            'fa-icon': 'eye'
        }

    def get_link_update_kwargs(self):
        return self.get_links_kwargs()

    def get_link_update(self):
        # TODO: i18n
        return {
            'name': 'Update',
            'href': reverse('{}update'.format(self.url_name), kwargs=self.get_link_update_kwargs()),
            'fa-icon': 'edit'
        }

    def get_link_delete_kwargs(self):
        return self.get_links_kwargs()

    def get_link_delete(self):
        return {
            'name': 'Delete',
            'href': reverse('{}delete'.format(self.url_name), kwargs=self.get_link_delete_kwargs()),
            #'fa-icon': 'trash', 'class': 'aconfirm'
            'fa-icon': 'trash'
        }

    @property
    def links(self):
        # TODO: diperiksa permission dan buat getter-nya agar los-coupling
        links = []
        for action in self.actions:
            method_name = 'get_link_{}'.format(action)
            if not hasattr(self, method_name):
                continue
            links.append(getattr(self, method_name)())
        return links

    def render(self, record, value):
        self.record = record
        html = []
        for link in self.links:
            html.append(
                T.a(
                    T.span(klass='fa fa-{}'.format(link['fa-icon'])),
                    href=link['href'], title=link['href'],
                    klass=link.get('class', '')
                )
            )

        return format_html('  '.join(html))
