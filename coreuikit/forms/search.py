from django import forms
from django.forms.models import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions, PrependedText
from crispy_forms.layout import Layout, Submit, Div, Button

from .fields import TextInlineFieldMixin


class BaseSearchField(object):
    """
    make all as optional (Disable all required fields)
    """

    def __init__(self, *args, **kwargs):
        kwargs['required'] = False
        return super().__init__(*args, **kwargs)


class CharField(BaseSearchField, TextInlineFieldMixin, forms.CharField):
    pass


class IntegerField(BaseSearchField, TextInlineFieldMixin, forms.IntegerField):
    pass


class LocalFormActions(FormActions):

    def render(self, form, form_style, context, *args, **kwargs):
        context['label_class'] = None
        return super().render(form, form_style, context, *args, **kwargs)


class BaseSearchForm(forms.Form):

    form_class = 'form-horizontal'
    form_id = None
    label_class = 'col-md-2'
    field_class = 'col-md-10'
    container_class = ''
    fields_container_class = 'row'
    buttons_container_class = 'row'
    right_field_class = 'col-md-6'
    left_field_class = 'col-md-6'

    display_args = {}

    def __init__(self, display_args={}, *args, **kwargs):
        self.display_args = display_args
        return super().__init__(*args, **kwargs)

    def gen_querset_filters(self, model):
        # default to set icontains if there is form fields that has a same name in model's attribute
        search = []
        kwsearch = {}
        form_data = self.cleaned_data
        for search_field, search_content in form_data.items():
            if not hasattr(model, search_field) or not search_content:
                continue
            search_key = '{}__icontains'.format(search_field)
            kwsearch[search_key] = search_content

        return (search, kwsearch)

    def filter(self, model):
        # filtering queryset for table data
        search, kwsearch = self.gen_querset_filters(model)
        queryset = model.objects.filter(*search, **kwsearch)
        return queryset

    @property
    def helper(self):
        # TODO: masukan translation disini
        helper = FormHelper()
        helper.form_method = 'GET'
        helper.form_class = self.form_class
        helper.form_id = self.form_id
        helper.label_class = self.label_class
        helper.field_class = self.field_class

        div_container = Div(css_class=self.container_class)
        fields_container = Div(css_class=self.fields_container_class)


        # populate field data
        div_fields_right = Div(css_class=self.right_field_class)
        div_fields_left = Div(css_class=self.left_field_class)

        counter = 0

        for name, field in self.fields.items():
            if counter % 2:
                div_fields = div_fields_left
            else:
                div_fields = div_fields_right

            div_fields.fields.append(
                PrependedText(name, field.display)
            )
            counter += 1

        fields_container.fields.append(div_fields_right)
        fields_container.fields.append(div_fields_left)

        buttons_container = LocalFormActions(
            Submit('search', 'Search', css_class='btn-primary'),
            Button('clear', 'Clear', css_class='btn-warning', css_id='btn_clear_searchform'),
            css_class=self.buttons_container_class
        )

        div_container.fields = [fields_container, buttons_container]
        helper.layout = Layout(div_container)
        return helper
