import sweetify
from django.views import generic
from django.utils.encoding import force_text
from .mixins import CoreUIViewMixin


class DeleteModelView(CoreUIViewMixin, generic.DeleteView):
    viewset = None
    coreui_template = 'confirm_delete.html'

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        # TODO: translation di perbaiki
        sweetify.success(request, 'Success', text='{} Successfully deleted'.format(
            force_text(self.object)
        ))
        return response

