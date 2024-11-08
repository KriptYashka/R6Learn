from django.contrib import admin
from appsite.models.models_map import MapModel


class AdminMap(admin.ModelAdmin):
    pass


admin.site.register(MapModel)
