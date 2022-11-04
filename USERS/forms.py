from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import profile
from django.core.validators import RegexValidator
import re


class registration_form (UserCreationForm):

        username= forms.CharField(widget=forms.TextInput(attrs={
            "type":"name",
            "id":"form1Example1",
            "class":"form-control"

        }))
        email = forms.EmailField(widget=forms.TextInput(attrs={
            "type":"email",
            "id":"form1Example1",
            "class":"form-control",
            "placeholder":"mwananchi@mail.com,"

        }))

        password1 = forms.CharField(widget=forms.TextInput(attrs={
            "type":"password",
            "id":"form1Example2",
            "class":"form-control",
            "placeholder":"********",
            "auto-complete":"off"
        }))

        password2 = forms.CharField(widget=forms.TextInput(attrs={
            "type":"password",
            "id":"form1Example2",
            "class":"form-control",
            "placeholder":"********",

        }))


        class Meta:
            model=User
            fields=[
            'username',
            'email',
            'password1',
            'password2',

            ]


class profileupadateform(forms.ModelForm):
    cell_number = forms.IntegerField(validators=[RegexValidator(r'^[0-9]{9}$', 'Enter a valid kenyan number')],
        widget=forms.TextInput(attrs={
        "type":"name",
        "id":"form1Example1",
        "class":"form-control",
        "placeholder":"",

    }))
    class Meta:
        model= profile
        fields=['cell_number']
