from django import forms

from appsite.models import Map


class FormMap(forms.ModelForm):
    class Meta:
        model = Map
        fields = '__all__'
