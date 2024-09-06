from django.contrib import admin
from django.urls import path

from appsite.views import main_views, profile_views, register_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_views.index_page),
    path('map/create/', main_views.create_map_page),
]
