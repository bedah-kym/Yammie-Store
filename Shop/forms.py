from django import forms
from django.db import models
from .validators import locationvalidation


PAYMENT_CHOICES=[
    ('LipanaMpesa','lipa na mpesa'),
    ('CashonDelivery','Cash on Deliverly')
]


class checkoutform(forms.Form):
    #l1=locationvalidation('street_name')
    street_name = forms.CharField(widget=forms.TextInput(attrs={
        "type":"name",
        "id":"address",
        "class":"form-control",
        "placeholder":"street/village name"

    }))

    sub_county = forms.CharField(widget=forms.TextInput(attrs={
        "type":"name",
        "id":"address",
        "class":"form-control"

    }))

    ward = forms.CharField(widget=forms.TextInput(attrs={
        "type":"name",
        "id":"address",
        "class":"form-control"

    }))
    payment_options = forms.ChoiceField(widget=forms.RadioSelect,choices=PAYMENT_CHOICES)



class promocodeform(forms.Form):
    p_code = forms.CharField(widget=forms.TextInput(attrs={
        "type":"text",
        "class":"form-control",
        "placeholder" : "Promo code ",
        "aria-label": "Recipient's username",
        "aria-describedby": "basic-addon2"

    }))

class commentform(forms.Form):
    text = forms.CharField(max_length=300,widget=forms.Textarea(attrs={
        "rows":3,
        "type":"text",
        "class":"form-control",
        "aria-label": "Recipient's username",
        "aria-describedby": "basic-addon2",
        "placeholder":" Hi, honest comments help people shop better B-) "

    }))
