from typing import List

from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render, redirect

from appsite.forms import FormMap
from appsite.forms.form_map import FormMapStats, FormPlace, FormPlaceImg
from appsite.models import MapModel, MapStatsModel, PlaceModel, PlaceImgModel

from django.shortcuts import get_object_or_404

from .tools.map import Map
from ..models.models_map import LevelModel


def index_page(request: WSGIRequest):
    template_name = "main/index.html"
    context = {}
    maps = MapModel.objects.all()
    context["maps"] = maps
    return render(request, template_name, context)


def map_create_page(request: WSGIRequest):
    template_name = "main/map_create.html"
    context = dict()
    if request.method == "GET":
        context["form"] = FormMap()
        return render(request, template_name, context)

    form = FormMap(request.POST, request.FILES)
    if form.is_valid():
        img = request.FILES["img"]  # TODO: Изменить название картинки
        instance_map = MapModel(title=form.data["title"].lower(), img=img)
        instance_map_stats = MapStatsModel(map=instance_map)

        instance_map.save()
        instance_map_stats.save()
        return redirect(f"/map/{instance_map.title.lower()}/info")
    else:
        context["errors"] = form.errors
    return render(request, template_name, context)


def map_edit_page(request: WSGIRequest, title: str):
    template_name = "main/map_edit.html"
    title = title.lower()

    curr_map = Map()
    curr_map.extract(title=title)

    map_data = {
        "title": curr_map.title,
    }
    map_stats_data = {
        "description": curr_map.stats.description,
        "win_atk": curr_map.stats.win_atk,
    }
    context = {
        "holder": curr_map.holder,
        "form_map": FormMap(map_data),
        "form_mapstat": FormMapStats(map_stats_data)
    }
    if request.method == "GET":
        return render(request, template_name, context)
    form_map, form_map_stats = FormMap(request.POST, request.FILES), FormMapStats(request.POST)
    new_title = check_forms(form_map, form_map_stats, title)

    return redirect(f"/map/edit/{new_title}")


def map_view_page(request: WSGIRequest, title: str):
    template_name = "main/map_view.html"
    current_map = get_object_or_404(MapModel, title=title.lower())

    levels_names = [LevelModel.BASEMENT, LevelModel.OUTSIDE, LevelModel.F1, LevelModel.F2, LevelModel.F3]
    levels = [
        {
            "name": name,
            "label": name.label,
            "places": PlaceModel.objects.filter(
                map=current_map,
                level=name
            ).prefetch_related('placeimgmodel_set')
        }
        for name in levels_names
    ]

    for level in levels:
        for place in level["places"]:
            place.first_img = place.placeimgmodel_set.first()

    context = {
        "map": current_map,
        "levels": levels,
    }
    return render(request, template_name, context)


def check_forms(form_map, form_map_stats, title):
    if form_map.is_valid():
        _title = form_map.data["title"]
        _img = form_map.files.get("img")
        map = MapModel.objects.get(title=title)
        map.name = _title
        if _img is not None:
            map.images = _img
        map.save()
        title = map.name
    if form_map_stats.is_valid():
        _description = form_map.data["description"]
        _win_atk = form_map.data["win_atk"]
        map = MapModel.objects.get(title=title)
        map_stat = MapStatsModel.objects.get(map=map)
        map_stat.description = _description
        map_stat.win_atk = _win_atk
        map_stat.save()
    return title


def place_create_page(request: WSGIRequest, map_title: str):
    template_name = "main/place_create.html"
    map_obj = get_object_or_404(MapModel, title=map_title.lower())
    context = {
        "map": map_obj,
        "form": FormPlace(),
    }
    if request.method == "GET":
        return render(request, template_name, context)

    form = FormPlace(request.POST)
    if form.is_valid():
        form.instance.map = map_obj
        form.save()
        return redirect(f"/map/{map_title}/info")
    context["form"] = form
    return render(request, template_name, context)


# def place_edit_page(request: WSGIRequest, img_id: int):
#     template_name = "main/place_edit.html"
#     place = PlaceModel.objects.get(id=img_id).prefetch_related('placeimgmodel_set')
#     context = {
#         "place": place,
#         "form": FormPlaceImg()
#     }
#     return render(request, template_name, context)

# Часть GPT


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


def update_place(request: WSGIRequest, place_id: int):
    place = get_object_or_404(PlaceModel, id=place_id)

    if request.method == 'POST':
        place.name = request.POST.get('name')
        place.description = request.POST.get('description')
        place.level = request.POST.get('level')
        place.is_layout = 'is_layout' in request.POST
        place.save()

    return redirect('place_edit', img_id=place.id)


def add_place_image(request: WSGIRequest, place_id: int):
    place = get_object_or_404(PlaceModel, id=place_id)

    if request.method == 'POST' and request.FILES.get('image'):
        PlaceImgModel.objects.create(
            place=place,
            img=request.FILES['image'],
            is_spectator=request.POST.get("is_spectator", False)
        )

    return redirect('place_edit', img_id=place.id)


def delete_place_image(request: WSGIRequest, image_id: int):
    image = get_object_or_404(PlaceImgModel, id=image_id)
    place_id = image.place.id
    image.delete()
    return redirect('place_edit', img_id=place_id)


def set_main_image(request: WSGIRequest, image_id: int):
    image = get_object_or_404(PlaceImgModel, id=image_id)
    # Логика установки основного изображения
    # (зависит от вашей реализации)
    return redirect('place_edit', img_id=image.place.id)
