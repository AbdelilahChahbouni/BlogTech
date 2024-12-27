from django.urls import path
from .views import *


urlpatterns = [
    path('list_or_craete' , post_list_create_api , name="post_list_create_api" ),
    path('details_update_delete/<int:pk>' , post_details_update_delete , name="post_details_update_delete"),
    path('post_like/<int:pk>' , post_like , name="post_like"),
    path('comments_list_create/<int:post_id>' , comment_list_create , name="comment_list_create"),
    path('register_api' , register , name="register_api"),
    path('login/' , login_api , name="login_api"),
    path('logout/' , logout_api , name="logout_api"),
    path('reset_password' , reset_password , name="reset_password"),
    path('reset_password_confirm' , reset_password_confirm , name="reset_password_confirm"),
    path('show_profile/<int:user_id>' , show_profile , name="show_profile"),
    path('edite_profile/<int:profile_id>' , edite_profile , name="edite_profile"),
    path('list_notification' , list_notification , name="get_notification"),
    path('read_notification/<int:id>' , read_notification , name="read_notification"),
    

]
