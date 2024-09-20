from django.contrib import admin
from appsite.models.models_map import Map


class AdminMap(admin.ModelAdmin):
    pass


admin.site.register(Map)
