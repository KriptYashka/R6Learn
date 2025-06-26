from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render, redirect, get_object_or_404

from appsite.forms import FormMap
from appsite.forms.form_map import FormMapStats
from appsite.models import MapModel, MapStatsModel
from appsite.views.gamemap.handlers import get_map_levels
from appsite.views.tools.map import Map, check_forms


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
        return redirect(f"/gamemap/{instance_map.title.lower()}/info")
    else:
        context["errors"] = form.errors
    return render(request, template_name, context)


def map_view_page(request: WSGIRequest, title: str):
    template_name = "main/map_view.html"
    current_map = get_object_or_404(MapModel, title=title.lower())

    levels = get_map_levels(current_map)

    context = {
        "gamemap": current_map,
        "levels": levels,
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

    return redirect(f"/gamemap/edit/{new_title}")
