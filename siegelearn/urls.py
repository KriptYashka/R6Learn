from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static

from appsite.views import main_views, profile_views, register_views
from siegelearn import settings

from appsite.views.api import map_api

urlpatterns = [
    path('admin/', admin.site.urls, name="admin"),
    path('', main_views.index_page, name="index"),
    path('map/create/', main_views.create_map_page, name="map_create"),
    path('map/<str:title>/info', main_views.map_view_page, name="map_view"),
    path('map/<str:title>/create', main_views.map_edit_page, name="map_edit"),
    path('map/<str:title>/place/edit', main_views.place_edit_page, name="place_edit"),

    path('api/map/', map_api.GetMapInfoView.as_view())
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
