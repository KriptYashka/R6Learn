from django.urls import path, include

from .handlers import add_place_image, update_place, set_main_image, delete_place_image
from .pages import place_create_page, place_edit_page

urlpatterns = [
    path("<str:gamemap_title>/create/", place_create_page, name="place_create"),
    path("<str:place_id>/edit/", place_edit_page, name="place_edit"),

    path("<int:place_id>/handler/add", add_place_image, name="handler_place_add"),
    path("<int:place_id>/handler/update", update_place, name="handler_place_update"),
    path("handler/image/set_main_image/<int:image_id>", set_main_image, name="handler_place_img_main"),
    path("handler/image/delete/<int:image_id>", delete_place_image, name="handler_place_img_delete"),
]