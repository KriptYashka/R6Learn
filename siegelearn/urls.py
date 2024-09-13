from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static

from appsite.views import main_views, profile_views, register_views
from siegelearn import settings

urlpatterns = [
    path('admin/', admin.site.urls, name="admin"),
    path('', main_views.index_page, name="index"),
    path('map/create/', main_views.create_map_page, name="map_create"),
    path('map/info/<str:title>', main_views.map_view_page, name="map_view"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
