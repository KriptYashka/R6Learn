from django import forms

from appsite.models import MapModel, MapStatsModel, PlaceModel, PlaceImgModel


class FormMap(forms.ModelForm):
    class Meta:
        model = MapModel
        fields = '__all__'
        widgets = {
            "img": forms.FileInput(attrs={"class": "form-control", "onchange": "preview(this)"}),
        }


class FormMapStats(forms.ModelForm):
    class Meta:
        model = MapStatsModel
        fields = ["description", "win_atk"]


class FormPlace(forms.ModelForm):
    class Meta:
        model = PlaceModel
        fields = ["name", "description", "level", "is_layout"]


class FormPlaceImg(forms.ModelForm):
    class Meta:
        model = PlaceImgModel
        fields = "__all__"
