from django.urls import path, include

urlpatterns = [
    path("", include("common.urls")),
    path("map/", include("gamemap.urls")),
    path("place/", include("place.urls")),
]