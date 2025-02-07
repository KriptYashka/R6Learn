from typing import List

from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render, redirect

from appsite.forms import FormMap
from appsite.forms.form_map import FormMapStats, FormPlace, FormPlaceImg
from appsite.models import MapModel, MapStatsModel, MapPlaceModel, MapPlaceImgModel

from django.shortcuts import get_object_or_404

from .tools.map import Map


def index_page(request: WSGIRequest):
    template_name = "main/index.html"
    context = {}
    maps = MapModel.objects.all()
    context["maps"] = maps
    return render(request, template_name, context)


def check_place_page(request: WSGIRequest, map_name: str):
    template_name = "main/map_place.html"
    context = {}
    return render(request, template_name, context)


def create_map_page(request: WSGIRequest):
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
    else:
        context["errors"] = form.errors
    return render(request, template_name, context)


def map_view_page(request: WSGIRequest, title: str):
    template_name = "main/map_view.html"
    current_map = get_object_or_404(MapModel, title=title.lower())
    context = {
        "map": current_map,
        "levels": [i for i in range(6)]
    }
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
    context = {}
    template_name = "main/place_create.html"
    map_obj = get_object_or_404(MapModel, title=map_title.lower())
    context = {
        "map": map_obj,
        "form": FormPlace,
    }
    return render(request, template_name, context)


def place_edit_page(request: WSGIRequest, title: str):
    template_name = "main/map_place_edit.html"
    map_obj = Map()
    map_obj.extract(title=title)
    context = {
        "map": map_obj,
        "form": FormPlaceImg()
    }
    return render(request, template_name, context)
