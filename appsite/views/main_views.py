from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render

from appsite.forms import FormMap
from appsite.models import Map


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

    form = FormMap(request.POST)
    if form.is_valid():
        title = form.data['title']
        img = form.data['img']
        Map(title=title, img=img).save()
    else:
        context["errors"] = form.errors
    return render(request, template_name, context)