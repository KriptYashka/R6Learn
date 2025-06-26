from appsite.models import PlaceModel
from appsite.models.models_map import LevelModel


def get_map_levels(current_map):
    levels_names = [LevelModel.BASEMENT, LevelModel.OUTSIDE, LevelModel.F1, LevelModel.F2, LevelModel.F3]
    levels = [
        {
            "name": name,
            "label": name.label,
            "places": PlaceModel.objects.filter(
                map=current_map,
                level=name
            ).prefetch_related('placeimgmodel_set')
        }
        for name in levels_names
    ]
    for level in levels:
        for place in level["places"]:
            place.first_img = place.placeimgmodel_set.first()
    return levels
