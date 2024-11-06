from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render

from appsite.forms import FormMap
from appsite.models import Map, MapStats

from django.shortcuts import get_object_or_404


# Create your views here.
def index_page(request: WSGIRequest):
    template_name = "main/index.html"
    context = {}
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
