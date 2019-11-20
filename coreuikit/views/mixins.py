import sweetify
from django.urls import reverse
from django.template import loader
from django.forms.models import modelform_factory
from ..forms.base import ModelFormBase
from coreuikit.utils.helper import Helper
from pprint import pprint


class TabsMixin(object):
    """
    Untuk kontent bisa diambil dari method get_content atau get_content_[NAMA_CURRENT_TAB]
    """
    active = None

    def render_template(self, template_name, context):
        content = loader.render_to_string(template_name, context, self.request, using=None)
        return content

    def get_tabs(self):
        """
        Example:
        (
            {'name': 'Summary', 'content': 'First tab'},
            {'name': 'Second', 'content': 'This is the first'},
            {'name': 'To Google', 'link': 'https://google.com'}
        )
        :return: list
        """
        return ()

    def get_active_tab(self):
        return self.active

    def filter_tab_contents(self, context):
        tabs = context['tabs']['list']
        active_tab = context['tabs']['active']

        result = []
        for tab in tabs:
            name = Helper.convert_flat(tab['name'])
            method = 'get_content_{}'.format(name)
            if hasattr(self, method):
                tab['content'] = getattr(self, method)(context)
            result.append(tab)

        context['tabs']['list'] = result
        return context

    def get_active_content(self, context=None):
        """
        Konten dari tab yg aktif
        :return:
        """
        return None

    def get_tabs_content(self, context):
        result = {}
        active_content = self.get_active_content(context)
        if active_content:
            result[self.get_active_tab()] = active_content

        for tab in self.get_tabs():
            name = Helper.convert_flat(tab['name'])
            method = 'get_content_{}'.format(name)
            if hasattr(self, method):
                result[name] = getattr(self, method)(context)
            elif 'content' in tab:
                result[name] = tab.get('content')
        return result

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'tabs': {
            'active': self.get_active_tab(),
            'list': self.get_tabs(),
            'contents': self.get_tabs_content(context),
        }})
        #pprint(context['tabs'])
        return context



class CoreUIViewMixin():

    coreui_template = None

    # TODO: mungkin ini bisa dimasukan dalam bentuk mixin untuk UpdateView
    # TODO: mengambalikan url ke arah yang detail
    # TODO: kirimkan flash messages jika succes atau error, pesan bisa di kustomisasi
    def get_success_url(self):
        if self.success_url is None:
            model_meta = self.model._meta
            # TODO: dibuat dengan namespace yang benar
            url_name = '{}:{}_list'.format(model_meta.app_label, model_meta.model_name)
            url_name = '{}_list'.format(model_meta.model_name)
            return reverse(url_name)
            return reverse(url_name, args=[self.object.pk])
        return super().get_success_url()

    def get_template_names(self):
        if self.template_name is None:
            #opts = self.object_list.model._meta
            opts = self.model._meta
            templates = [
                '{}/{}{}.html'.format(
                    opts.app_label,
                    opts.model_name,
                    self.template_name_suffix),
            ]
            if self.coreui_template:
                templates.append(
                    'coreuikit/views/{}'.format(self.coreui_template),
                )

            return templates
        return [self.template_name]


class FormMixin(CoreUIViewMixin):

    template_name_suffix = '_form'

    exclude = ()

    def get_form_class(self):
        if self.form_class:
            return self.form_class

        return modelform_factory(self.model,
                                 form=ModelFormBase,
                                 fields=self.fields,
                                 exclude=self.exclude)

    def form_invalid(self, form):
        # masukan ke flash message untuk error-nya
        response = super().form_invalid(form)
        #print(form.errors)
        sweetify.error(self.request, 'Error', text='The data not valid')
        return response

    def form_valid(self, form):
        response = super().form_valid(form)
        sweetify.success(self.request, 'Success', text='The data was added')
        return response
