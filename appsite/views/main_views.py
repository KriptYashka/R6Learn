from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render

# Create your views here.
def index_page(request: WSGIRequest):
    template_name = "main/index.html"
    context = {}
    return render(request, template_name, context)