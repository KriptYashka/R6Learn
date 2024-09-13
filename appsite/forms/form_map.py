from django import forms


class FormMap(forms.Form):
    title = forms.CharField(max_length=32)
    img = forms.ImageField(allow_empty_file=True)
