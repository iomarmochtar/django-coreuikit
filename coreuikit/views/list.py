from django.views.generic.base import ContextMixin, TemplateResponseMixin
from django.views.generic import View
from django.urls import reverse
from django.contrib.auth import get_permission_codename
from django_tables2 import RequestConfig


class DataMixin(ContextMixin):

    viewset = None
    search_form_class = None
    # TODO: protes jika table class tidak ada
    table_class = None
    # TODO: dibetulkan menjadi table_requestconfig_args
    table_requestconfig_args = {}

    def get(self, request, *args, **kwargs):
        """Response with rendered html template."""
        context = self.get_context_data()
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        # inject data tabel
        context = super().get_context_data(**kwargs)
        inject = {'search_form': None}

        if self.search_form_class:
            inject['search_form'] = self.search_form_class(data=self.request.GET)

        # TODO: lakukan pencarian jika form adalah valid
        inject['table'] = self.table_class(
            self.get_queryset(inject['search_form'])
        )

        RequestConfig(self.request, **self.table_requestconfig_args).configure(
            inject['table'])

        context.update(inject)
        return context

    def get_queryset(self, search_form=None):
        if not search_form:
            return self.model.objects.all()

        if not search_form.is_valid():
            # TODO: Show flash message for any errors in search form
            return self.model.objects.none()

        return search_form.filter(self.model)


class ListModelView(TemplateResponseMixin, DataMixin, View):
    model = None
    queryset = None
    template_name_suffix = '_list'

    def has_view_permission(self, request, obj=None):
        """Object view permission check.

        If view had a `viewset`, the `viewset.has_view_permission` used.
        """
        if self.viewset is not None:
            return self.viewset.has_view_permission(request, obj)

        # default lookup for the django permission
        opts = self.model._meta
        codename = get_permission_codename('view', opts)
        view_perm = '{}.{}'.format(opts.app_label, codename)
        if request.user.has_perm(view_perm):
            return True
        elif request.user.has_perm(view_perm, obj=obj):
            return True
        return self.has_change_permission(request, obj=obj)

    def has_change_permission(self, request, obj=None):
        """Object change permission check.

        If view had a `viewset`, the `viewset.has_change_permission` used.
        """
        if self.viewset is not None:
            return self.viewset.has_change_permission(request, obj)

        # default lookup for the django permission
        opts = self.model._meta
        codename = get_permission_codename('change', opts)
        change_perm = '{}.{}'.format(opts.app_label, codename)
        if request.user.has_perm(change_perm):
            return True
        return request.user.has_perm(change_perm, obj=obj)

    def has_add_permission(self, request):
        """Object add permission check.

        If view had a `viewset`, the `viewset.has_add_permission` used.
        """
        if self.viewset is not None:
            return self.viewset.has_add_permission(request)

        # default lookup for the django permission
        opts = self.model._meta
        codename = get_permission_codename('add', opts)
        return request.user.has_perm('{}.{}'.format(opts.app_label, codename))

    def get_add_url(self):
        meta = self.model._meta
        return reverse('{}_add'.format(meta.model_name))

    def get_context_data(self, **kwargs):

        #opts = self.model._meta
        if self.has_add_permission(self.request):
            #kwargs['add_url'] = reverse('{}:{}_add'.format(opts.app_label, opts.model_name))
            #kwargs['add_url'] = reverse('{}_add'.format(opts.model_name))
            kwargs['add_url'] = self.get_add_url()

        return super(ListModelView, self).get_context_data(**kwargs)

    def get_template_names(self):
        if self.template_name is None:
            #opts = self.object_list.model._meta
            opts = self.model._meta
            return [
                '{}/{}{}.html'.format(
                    opts.app_label,
                    opts.model_name,
                    self.template_name_suffix),
                'coreuikit/views/list.html',
            ]
        return [self.template_name]

