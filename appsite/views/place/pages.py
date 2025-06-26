from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import get_object_or_404, render, redirect

from appsite.forms.form_map import FormPlace
from appsite.models import PlaceModel, MapModel
from appsite.models.models_map import LevelModel


def place_create_page(request: WSGIRequest, map_title: str):
    template_name = "main/place_create.html"
    map_obj = get_object_or_404(MapModel, title=map_title.lower())
    context = {
        "map": map_obj,
        "form": FormPlace(),
    }

    if request.method == "POST":
        form = FormPlace(request.POST)
        if form.is_valid():
            form.instance.map = map_obj
            form.save()
            return redirect(f"/map/{map_title}/info")
        context["form"] = form

    return render(request, template_name, context)


def place_edit_page(request: WSGIRequest, img_id: int):
    template_name = "main/place_edit.html"
    place = get_object_or_404(PlaceModel.objects.prefetch_related('placeimgmodel_set'), id=img_id)

    context = {
        "place": place,
        "levels": [
            (LevelModel.BASEMENT.value, LevelModel.BASEMENT.label),
            (LevelModel.OUTSIDE.value, LevelModel.OUTSIDE.label),
            (LevelModel.F1.value, "1 этаж"),
            (LevelModel.F2.value, "2 этаж"),
            (LevelModel.F3.value, "3 этаж"),
        ]
    }
    return render(request, template_name, context)
