from django.views import generic
from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe
from ..utils.simpletag import SimpleTag as T, Helpers as H

# TODO: translation


class DetailModelView(generic.DetailView):
    viewset = None

    def get_object_data(self):
        for field in self.object._meta.fields:
            # ignore auto increments field
            if isinstance(field, models.AutoField) or field.auto_created:
                continue

            alternate_display_attr = 'get_{}_display'.format(field.name)
            if hasattr(self.object, alternate_display_attr):
                value = getattr(self.object, alternate_display_attr)()
            else:
                value = getattr(self.object, field.name)

            if value is not None:
                yield (field.verbose_name.title(), value)

    def get_context_data(self, **kwargs):
        opts = self.model._meta
        kwargs['object_data'] = self.get_object_data()
        # TODO: masukan change_url dan delete_url sesuai dengan permission

        # TODO: diset lebih mudah untuk setting judul
        kwargs['card_header'] = self.object

        buttons = [
            T.a('Update', klass='btn btn-primary'),
            T.a('Delete', klass='btn btn-danger'),
        ]

        kwargs['card_footer'] = H.components(*buttons)

        return super().get_context_data(**kwargs)

    def get_template_names(self):
        if self.template_name:
            return [self.template_name]

        opts = self.model._meta
        return [
            '{}/{}{}'.format(
                opts.app_label,
                opts.model_name,
                self.template_name_suffix
            ),
            'coreuikit/views/detail.html'
        ]
