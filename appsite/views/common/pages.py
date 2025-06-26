from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render

from appsite.models import MapModel


def index_page(request: WSGIRequest):
    template_name = "main/index.html"
    context = {}
    maps = MapModel.objects.all()
    context["maps"] = maps
    return render(request, template_name, context)
