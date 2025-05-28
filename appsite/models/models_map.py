import os

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from django.utils.translation import gettext_lazy


def get_place_img_upload_path(instance, filename: str):
    return f"maps/{instance.place.map.title}/{instance.place.level}/{filename}"


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
    UNKNOWN = "NUL", "N/A"
    BASEMENT = "B", "Подвал"
    OUTSIDE = "OUT", "Снаружи"
    F1 = "1F", "Первый этаж"
    F2 = "2F", "Второй этаж"
    F3 = "3F", "Третий этаж"


class PlaceModel(models.Model):
    """
    Определенное место/позиция на карте
    """
    objects = models.Manager()
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
