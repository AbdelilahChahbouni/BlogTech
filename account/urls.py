
from django.urls import path , include
from .views import *

urlpatterns = [
    path('' , include("django.contrib.auth.urls")),
    path('register/' , register , name="register"),
    path('edite_profile/' , edit_profile , name="edite_profile"),
    path('show_profile/<int:user_id>' , show_profile , name="show_profile"),
    path('follow_unfollow/<int:author_id>' , follow_unfollow , name="follow_unfollow"),
]

