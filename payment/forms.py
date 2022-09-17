from django import forms


class payment_form (forms.Form):

        phone_number = forms.CharField(widget=forms.TextInput(attrs={
            "type":"name",
            "id":"form1Example1",
            "class":"form-control"

        }))
        
