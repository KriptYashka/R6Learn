from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import get_object_or_404, redirect

from appsite.models import PlaceModel, PlaceImgModel


def add_place_image(request: WSGIRequest, place_id: int):
    place = get_object_or_404(PlaceModel, id=place_id)

    if request.method == 'POST' and request.FILES.get('image'):
        PlaceImgModel.objects.create(
            place=place,
            img=request.FILES['image'],
            is_spectator=request.POST.get("is_spectator", False)
        )

    return redirect('place_edit', img_id=place.id)


def update_place(request: WSGIRequest, place_id: int):
    place = get_object_or_404(PlaceModel, id=place_id)

    if request.method == 'POST':
        place.name = request.POST.get('name')
        place.description = request.POST.get('description')
        place.level = request.POST.get('level')
        place.is_layout = 'is_layout' in request.POST
        place.save()

    return redirect('place_edit', img_id=place.id)


def set_main_image(request: WSGIRequest, image_id: int):
    image = get_object_or_404(PlaceImgModel, id=image_id)
    return redirect('place_edit', img_id=image.place.id)


def delete_place_image(request: WSGIRequest, image_id: int):
    image = get_object_or_404(PlaceImgModel, id=image_id)
    place_id = image.place.id
    image.delete()
    return redirect('place_edit', img_id=place_id)
