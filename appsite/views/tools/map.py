import logging
from typing import Optional

from django.db import models as dj_models
from appsite import models


class ModelETL:
    model: Optional[dj_models.Model] = None

    def __init__(self):
        pass

    def extract(self, **kwargs):
        pass

    def _get(self, model=None, **kwargs):
        model = model or self.model
        return model.objects.get(**kwargs)

    def _filter(self, model=None, **kwargs):
        model = model or self.model
        return model.objects.filter(**kwargs)


class Map(ModelETL):
    model = models.MapModel

    def __init__(self):
        super().__init__()
        self.title = None
        self.holder = None
        self.stats = None
        self.places = []
        self.instance = None

    def extract(self, **kwargs):
        self.instance: Map.model = self._get(**kwargs)
        self.title, self.holder = self.instance.title, self.instance.img

        self.stats = MapStats(self)
        try:
            self.stats.extract()
        except:
            logging.warning(f"Статистика карты {self.instance.id}: {self.instance.title} не найдена.")

        places = MapPlace.model.objects.filter(map__id=self.instance.id)
        for instance in places:
            place = MapPlace(self)
            place.transform(instance)
            self.places.append(place)


class MapStats(ModelETL):
    model = models.MapStatsModel

    def __init__(self, map_obj: Map):
        super().__init__()
        self.map = map_obj
        self.description = None
        self.win_atk = -1
        self.win_def = -1

    def extract(self, **kwargs):
        instance_stats: MapStats.model = self._get(map__id=self.map.instance.id)
        self.description = instance_stats.description
        self.win_atk, self.win_def = instance_stats.win_atk, instance_stats.win_def


class MapPlace(ModelETL):
    model = models.MapPlaceModel

    def __init__(self, map_obj: Map):
        super().__init__()
        self.map = map_obj
        self.name = None
        self.description = None
        self.level = None
        self.is_layout = None
        self.images = []

    def extract(self, **kwargs):
        images = MapPlaceImage.model.objects.filter(**kwargs)
        for instance in images:
            img = MapPlaceImage(self.map)
            img.transform(instance)
            self.images.append(img)

    def transform(self, instance: models.MapPlaceModel):
        self.map = instance.map
        self.description = instance.description
        self.level = instance.level
        self.is_layout = instance.is_layout


class MapPlaceImage(ModelETL):
    model = models.MapPlaceImgModel

    def __init__(self, map_obj: Map):
        super().__init__()
        self.map = map_obj
        self.img = None
        self.is_spectator = None

    def transform(self, instance: models.MapPlaceImgModel):
        self.img = instance.img
        self.is_spectator = instance.is_spectator
