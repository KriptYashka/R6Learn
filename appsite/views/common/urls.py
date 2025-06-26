from django.urls import path, include
from .pages import index_page

urlpatterns = [
    path("", index_page, name="main"),
]