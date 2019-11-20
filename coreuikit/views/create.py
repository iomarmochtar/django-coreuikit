from django.views import generic
from .mixins import FormMixin


class CreateModelView(FormMixin, generic.CreateView):

    template_name_suffix = '_create'
    coreui_template = 'create.html'
    exclude = ()

