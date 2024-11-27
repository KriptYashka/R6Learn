from django import forms

from appsite.models import MapModel, MapStatsModel, MapPlaceModel, MapPlaceImgModel


class FormMap(forms.ModelForm):
    class Meta:
        model = MapModel
        fields = '__all__'

class FormMapStats(forms.ModelForm):
    class Meta:
        model = MapStatsModel
        fields = ["description", "win_atk"]

class FormPlace(forms.ModelForm):
    class Meta:
        model = MapPlaceModel
        fields = ["name", "description", "level", "is_layout"]

class FormPlaceImg(forms.ModelForm):
    class Meta:
        model = MapPlaceImgModel
        fields = ["img", "is_spectator"]