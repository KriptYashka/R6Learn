import os

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from django.utils.translation import gettext_lazy


def get_place_img_upload_path(instance, filename: str):
    return f"maps/{instance.place.map.name}/{instance.place.level}/{filename}"


class MapModel(models.Model):
    title = models.CharField(max_length=32)
    img = models.ImageField(upload_to="maps/holders", blank=True)


class MapStatsModel(models.Model):
    map = models.ForeignKey(MapModel, models.CASCADE)
    description = models.CharField(max_length=2000, null=True)
    win_atk = models.IntegerField(null=True)
    win_def = models.IntegerField(null=True)


class LevelModel(models.TextChoices):
    """
    Перечисление этажей карты.
    `gettext_lazy` позволяет выполнить перевод
    """
    UNKNOWN = "NUL", gettext_lazy("Not defined")
    BASEMENT = "B", gettext_lazy("Basement")
    OUTSIDE = "OUT", gettext_lazy("Outside")
    F1 = "1F", gettext_lazy("First floor")
    F2 = "2F", gettext_lazy("Second floor")
    F3 = "3F", gettext_lazy("Third floor")


class PlaceModel(models.Model):
    """
    Определенное место/позиция на карте
    """
    map = models.ForeignKey(MapModel, models.CASCADE)
    name = models.CharField(max_length=32)
    description = models.CharField(max_length=300)
    level = models.CharField(
        max_length=3,
        choices=LevelModel.choices,
        default=LevelModel.UNKNOWN,
    )
    is_layout = models.BooleanField(blank=True, null=False, default=False)


class PlaceImgModel(models.Model):
    """
    Изображение места
    """

    place = models.ForeignKey(PlaceModel, models.CASCADE)
    img = models.FileField(upload_to=get_place_img_upload_path)

    # Порядок отображения
    is_spectator = models.BooleanField(blank=True, null=False, default=False)
