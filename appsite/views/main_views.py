from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render, redirect

from appsite.forms import FormMap
from appsite.forms.form_map import FormMapStats
from appsite.models import Map, MapStats

from django.shortcuts import get_object_or_404


# Create your views here.
def index_page(request: WSGIRequest):
    template_name = "main/index.html"
    context = {}
    maps = Map.objects.all()
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
        instance_map = Map(title=form.data["title"].lower(), img=img)
        instance_map_stats = MapStats(map=instance_map)

        instance_map.save()
        instance_map_stats.save()
    else:
        context["errors"] = form.errors
    return render(request, template_name, context)


def map_view_page(request: WSGIRequest, title: str):
    template_name = "main/map_view.html"
    current_map = get_object_or_404(Map, title=title.lower())
    context = {
        "map": current_map,
        "levels": [i for i in range(6)]
    }
    return render(request, template_name, context)

def map_edit_page(request: WSGIRequest, title: str):
    template_name = "main/map_edit.html"
    title = title.lower()
    current_map: Map = get_object_or_404(Map, title=title)
    current_map_stats: MapStats = MapStats.objects.get(map=current_map)
    map_data = {
        "title": current_map.title,
    }
    map_stats_data = {
        "description": current_map_stats.description,
        "win_atk": current_map_stats.win_atk,
    }
    context = {
        "holder": current_map.img,
        "form_map": FormMap(map_data),
        "form_mapstat": FormMapStats(map_stats_data),
    }
    if request.method == "GET":
        return render(request, template_name, context)
    form_map, form_map_stats = FormMap(request.POST, request.FILES), FormMapStats(request.POST)
    if form_map.is_valid():
        _title = form_map.data["title"]
        _img = form_map.files.get("img")
        map = Map.objects.get(title=title)
        map.title = _title
        if _img is not None:
            map.img = _img
        map.save()
        title = map.title
    if form_map_stats.is_valid():
        _description = form_map.data["description"]
        _win_atk = form_map.data["win_atk"]
        map = Map.objects.get(title=title)
        map_stat = MapStats.objects.get(map=map)
        map_stat.description = _description
        map_stat.win_atk = _win_atk
        map_stat.save()
    return redirect(f"/map/edit/{title}")

