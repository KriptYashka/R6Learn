from django.urls import path, include

from .pages import map_create_page, map_view_page, map_edit_page

urlpatterns = [
    path("create/", map_create_page, name="map_create"),
    path("<str:title>/info", map_view_page, name="map_view"),
    path("<str:title>/edit", map_edit_page, name="map_edit"),
]