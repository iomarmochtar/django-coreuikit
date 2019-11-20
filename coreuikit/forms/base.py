from django import forms
from .search import CharField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Button


class Base(object):
    horizontal_layout = False
    method = 'POST'
    html_id = None
    html_css = None
    action = None
    buttons = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.buttons = self.get_buttons()
        self.helper = self.get_helper()

    def get_buttons(self):
        return [
            Submit('submit', 'Submit'),
        ]

    def get_helper(self):
        helper = FormHelper()
        if self.html_id:
            helper.form_id = self.html_id

        if self.html_css:
            helper.form_class = self.html_css

        if self.action:
            helper.form_action = self.action

        helper.form_method = self.method

        for button in self.buttons:
            helper.add_input(button)

        if self.horizontal_layout:
            helper.form_class = 'form-horizontal'
            helper.label_class = 'col-md-2'
            helper.field_class = 'col-md-10'

        return helper


class FormBase(Base, forms.Form):
    pass


class ModelFormBase(Base, forms.ModelForm):
    pass