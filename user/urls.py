from django.urls import path
from .import views as v

urlpatterns =[
    path("my-found-items/", v.my_found_items, name="my_found_items"),
    path("delete-found-item/<int:item_id>/", v.delete_found_item, name="delete_found_item"),
]