from django import forms
from django.core.validators import RegexValidator

class payment_form (forms.Form):

        phone_number = forms.CharField(validators=[RegexValidator(r'^[0-9]{10}$', 'Enter a valid kenyan number/dont use +254')],widget=forms.TextInput(attrs={
            "type":"name",
            "id":"form1Example1",
            "class":"form-control",
            "placeholder":"phone number"

        }))
