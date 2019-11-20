from django.views import generic
from .mixins import FormMixin


class UpdateModelView(FormMixin, generic.UpdateView):
    template_name_suffix = '_update'
    coreui_template = 'update.html'

