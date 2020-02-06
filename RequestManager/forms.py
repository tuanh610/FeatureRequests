from django.urls import reverse
from django import forms
from .models import Request, ClientDetail
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Button

class RequestForm(forms.ModelForm):

    class Meta:
        model = Request
        fields = ('client', 'description', 'client_priority', 'target_date', 'product_area')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 20, 'cols': 50}),
            'target_date': forms.TextInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('RequestManager:new_request')
        self.helper.layout = Layout(
            Row(
                Column('client', css_class='col s3'),
                Column('client_priority', css_class='col s3'),
                Column('target_date', css_class='col s6')
            ),
            Row(
                Column('product_area', css_class='col s12'),
            ),
            Row(
                Column('description', css_class='col s12'),
            ),
            Row(
                Submit('submit', "Submit", css_class="waves-effect waves-light")
            )
        )
