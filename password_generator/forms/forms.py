from django import forms

class PasswordGeneratorForm(forms.Form):

    number_of_char = forms.IntegerField()

    widget = {
        'number_of_char': forms.NumberInput( attrs={'type':'number', 'min': '6', 'max': '99'}),
    }