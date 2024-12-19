from django.urls import path
from .views import *


urlpatterns = [
    path('list_or_craete' , post_list_create_api , name="post_list_create_api" ),
    path('details_update_delete/<int:pk>' , post_details_update_delete , name="post_details_update_delete"),
    path('post_like/<int:pk>' , post_like , name="post_like"),
    path('comments_list_create/<int:post_id>' , comment_list_create , name="comment_list_create"),
]
