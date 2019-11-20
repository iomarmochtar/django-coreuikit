from django.conf.urls import url
from django.contrib.auth import get_permission_codename
from django.forms.models import modelform_factory
from django.forms.formsets import formset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import  Layout, Submit, Div
from crispy_forms.bootstrap import FormActions
from .list import ListModelView
from .create import CreateModelView
from .detail import DetailModelView
from .update import UpdateModelView
from .delete import DeleteModelView
#from ..forms.base import BaseModelForm, BaseSearchModelForm
#from ..forms.base import BaseSearchForm
from ..forms.search import BaseSearchForm
from ..forms.factory import form_factory
from ..tables.factory import table_class_factory

# testing
from django.http import HttpResponse

def test(request):
    return HttpResponse('Hello world')

DEFAULT = object()


class ModelViewSet(object):
    model = None
    search_form_class = None
    search_form_fields = ()
    search_form_fields_class = {}
    # TODO: autopopulate jika kosong
    table_class = None
    table_requestconfig_args = {'paginate': {'per_page': 10}}
    # TODO: listing fields untuk table
    # Untuk form dapat dibuat custom


    queryset = DEFAULT
    list_display = DEFAULT
    list_display_class = {}

    form_class = None
    form_fields = '__all__'
    form_fields_exclude = ()
    # TODO: tambahkan opsi untuk set form class (horizontal), dll
    form_widgets = None

    @property
    def urls(self):

        format_kwargs = {
            'model_name': self.model._meta.model_name
        }

        result = []
        url_entries = (
            getattr(self, attr)
            for attr in dir(self)
            if attr.endswith('_view')
            if isinstance(getattr(self, attr), (list, tuple))
        )
        for url_entry in url_entries:
            regexp, view, name = url_entry
            result.append(
                url(regexp.format(**format_kwargs),
                    view,
                    name=name.format(**format_kwargs))
            )

        return result

    def filter_kwargs(self, view_class, **kwargs):
        result = {
            'model': self.model,
            'viewset': self,
            'queryset': self.queryset,
        }
        result.update(kwargs)
        return {name: value for name, value in result.items()
                if hasattr(view_class, name)
                if value is not DEFAULT}

    ## Permission check

    def has_add_permission(self, request):
        """Default add permission check for a detail and list views.

        May not be called if views have own implementation.
        """
        return True
        opts = self.model._meta
        codename = get_permission_codename('add', opts)
        return request.user.has_perm('{}.{}'.format(opts.app_label, codename))

    def has_view_permission(self, request, obj=None):
        """Default view permission check for a detail and list views.

        May not be called if views have own implementation.
        """
        return True
        opts = self.model._meta
        codename = get_permission_codename('view', opts)
        view_perm = '{}.{}'.format(opts.app_label, codename)
        if request.user.has_perm(view_perm):
            return True
        elif request.user.has_perm(view_perm, obj=obj):
            return True
        return self.has_change_permission(request, obj=obj)

    def has_change_permission(self, request, obj=None):
        """Default change permission check for a update view.

        May not be called if update view have own implementation.
        """
        return True
        opts = self.model._meta
        codename = get_permission_codename('change', opts)
        change_perm = '{}.{}'.format(opts.app_label, codename)
        if request.user.has_perm(change_perm):
            return True
        return request.user.has_perm(change_perm, obj=obj)


    """
    List
    """
    list_view_class = ListModelView

    def get_list_view(self):
        """Function view for objects list."""
        return self.list_view_class.as_view(**self.get_list_view_kwargs())

    def get_search_form_class(self):
        """
        Mendapatkan form class
        :return:
        """
        # jika diset maka langsung balikan
        if self.search_form_class:
            return self.search_form_class
        elif not self.search_form_fields:
            return None

        # menjalankan form wizard
        form_class = form_factory(
            form_class=BaseSearchForm,
            fields=self.search_form_fields,
            fields_class=self.search_form_fields_class
        )
        return form_class

    def get_table_class(self):
        if self.table_class:
            return self.table_class

        table_class = table_class_factory(
            model=self.model,
            model_fields=self.list_display,
            fields_class=self.list_display_class
        )
        return table_class

    def get_list_view_kwargs(self, **kwargs):
        """Configuration arguments for list view.

        May not be called if `get_list_view` is overridden.
        """
        result = {
            'search_form_class': self.get_search_form_class(),
            'table_class': self.get_table_class(),
            'table_requestconfig_args': self.table_requestconfig_args
        }
        result.update(kwargs)
        return self.filter_kwargs(self.list_view_class, **result)

    @property
    def list_view(self):
        """Triple (regexp, view, name) for list view url config."""
        return [
            '^$',
            self.get_list_view(),
            '{model_name}_list'
        ]

    """
    Create
    """
    create_view_class = CreateModelView

    def get_create_view(self):
        """Function view for create an object."""
        return self.create_view_class.as_view(**self.get_create_view_kwargs())

    def get_form_class(self):
        return self.form_class

    def get_create_view_kwargs(self, **kwargs):
        # TODO: custom form agar eye caching
        inject = {}
        form_class = self.get_form_class()
        if form_class:
            inject['form_class'] = form_class
        else:
            inject['fields'] = self.form_fields
            inject['exclude'] = self.form_fields_exclude
            # TODO: tambahkan yang exclude
        kwargs.update(inject)
        return self.filter_kwargs(self.create_view_class, **kwargs)

    @property
    def create_view(self):
        """Triple (regexp, view, name) for list view url config."""
        return [
            '^add$',
            self.get_create_view(),
            '{model_name}_add'
        ]

    ###
    # Detail view
    ###
    detail_view_class = DetailModelView

    def get_detail_view(self):
        """Function view for create an object."""
        return self.detail_view_class.as_view(**self.get_detail_view_kwargs())

    def get_detail_view_kwargs(self, **kwargs):
        return self.filter_kwargs(self.detail_view_class, **kwargs)

    @property
    def detail_view(self):
        """Triple (regexp, view, name) for list view url config."""
        return [
            '^(?P<pk>\d+)/detail$',
            self.get_detail_view(),
            '{model_name}_detail'
        ]

    """
    Update
    """
    update_view_class = UpdateModelView

    def get_update_view(self):
        return self.update_view_class.as_view(**self.get_create_view_kwargs())

    def get_update_view_kwargs(self, **kwargs):
        # TODO: custom form agar eye caching
        inject = {}
        form_class = self.get_form_class()

        if form_class:
            inject['form_class'] = form_class
        else:
            inject['fields'] = self.form_fields
            inject['exclude'] = self.form_fields_exclude
        kwargs.update(inject)
        return self.filter_kwargs(self.update_view_class, **kwargs)

    @property
    def update_view(self):
        return [
            '^(?P<pk>\d+)/update$',
            self.get_update_view(),
            '{model_name}_update'
        ]

    """
    Delete 
    """
    delete_view_class = DeleteModelView

    def get_delete_view(self):
        return self.delete_view_class.as_view(**self.get_delete_view_kwargs())

    def get_delete_view_kwargs(self, **kwargs):
        return self.filter_kwargs(self.delete_view_class, **kwargs)

    @property
    def delete_view(self):
        return [
            '^(?P<pk>\d+)/delete$',
            self.get_delete_view(),
            '{model_name}_delete'
        ]
