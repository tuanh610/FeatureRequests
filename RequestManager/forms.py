""" This file holds all the forms that is used in the application

There are mainly 2 types of forms:
1.forms.Form which is custom form
2. forms.ModelForm which used the existing models to create form

For this project, we will use cripsy_form helper and layout
1. The helper generate the form html page faster and with ease
2. The layout will help control the layout of the elements in the form
"""
from django.urls import reverse
from django import forms
from .models import Request, ClientDetail
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Button
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RequestForm(forms.ModelForm):
    """
    A class used to represent the Request Input form

    ...

    Attributes
    ----------
    Meta : class
        defines how class is behaved

    Methods
    -------
    __init__(self, *args, **kwargs):
        Initialisation of the class
    """

    class Meta:
        """
        Custom Meta class which change how the class will behave
        ...

        Attributes
        ----------
        model : model.Models
            The model in which the forms will be constructed
        fields : tuple
            the name of the fields to shows in the forms (same name with the fields's name in the models)
        widgets : [Field.widget]
            widgets to change the behaviors of each fields in the input form
        """
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


class UserRegisterForm(UserCreationForm):
    """
    A class used to represent the user register form
    """
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
