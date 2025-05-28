from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static

from appsite.views import main_views, profile_views, register_views
from siegelearn import settings

from appsite.views.api import map_api

urlpatterns = [
    path('admin/', admin.site.urls, name="admin"),
    path('', main_views.index_page, name="index"),
    path('map/create/', main_views.map_create_page, name="map_create"),
    path('map/<str:title>/info', main_views.map_view_page, name="map_view"),
    path('map/<str:title>/create', main_views.map_edit_page, name="map_edit"),
    path('map/<str:map_title>/place/create', main_views.place_create_page, name="create_place"),

    path('place/<int:img_id>/edit/', main_views.place_edit_page, name='place_edit'),
    path('place/<int:place_id>/update/', main_views.update_place, name='update_place'),
    path('place/<int:place_id>/add-image/', main_views.add_place_image, name='add_place_image'),
    path('place-image/<int:image_id>/delete/', main_views.delete_place_image, name='delete_place_image'),
    path('place-image/<int:image_id>/set-main/', main_views.set_main_image, name='set_main_image'),

    path('api/map/', map_api.GetMapInfoView.as_view())
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
