from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render

from appsite.forms import FormMap
from appsite.models import Map

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
    context = {
        "form": FormMap(request.GET)
    }
    if request.method == "GET":
        return render(request, template_name, context)
    # print(request.POST)
    form = FormMap(request.POST)
    # print(form)
    # print(f"{form.is_valid()} - валидность формы")
    # print(f"{form.errors} - ошибки")
    if True:
        title = form.data['title'].lower()
        img = form.data['img']
        Map(title=title, img=img).save()
    else:
        context["errors"] = form.errors
    return render(request, template_name, context)


def map_view_page(request: WSGIRequest, title: str):
    template_name = "main/map_view.html"
    current_map = get_object_or_404(Map, title=title.lower())
    context = {
        "map": current_map
    }
    return render(request, template_name, context)