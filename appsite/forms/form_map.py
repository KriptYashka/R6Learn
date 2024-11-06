from django import forms

from appsite.models import Map, MapStats


class FormMap(forms.ModelForm):
    class Meta:
        model = Map
        fields = '__all__'

class FormMapStats(forms.ModelForm):
    class Meta:
        model = MapStats
        fields = '__all__'
