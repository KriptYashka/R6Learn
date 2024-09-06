from django import forms

class FormMap(forms.Form):
    title = forms.CharField(max_length=32, required=True)
    img = forms.ImageField(allow_empty_file=True, required=True)