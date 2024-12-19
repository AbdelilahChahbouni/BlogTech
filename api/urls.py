from django.urls import path
from .views import *


urlpatterns = [
    path('list_or_craete' , post_list_create_api , name="post_list_create_api" ),
    path('details_update_delete/<int:pk>' , post_details_update_delete , name="post_details_update_delete"),
]
