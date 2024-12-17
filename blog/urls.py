from django.urls import path 
from .views import *
from django.shortcuts import render


urlpatterns = [
    path('' , default , name="default"),
    path('posts/' , home , name="home"),
    path('author_posts/' , author_posts , name="author_posts"),
    path('about/' , about , name="about"),
    path('contact/' , contact , name="contact"),
    path('post_details/<slug:post>/' , post_details , name="post_details"),
    path('create_post/' , create_post , name='create_post'),
    path('delete_post/<int:post_id>/' , delete_post , name="delete_post"),
    path('update_post/<int:post_id>/' , update_post , name="update_post"),
    path('post_comment/' , post_comment , name="post_comment"),
    path('post_like/', post_like, name="post_like"),
    path('contact_user/' , contact_view , name="contact_user"),
    path('notification/read/<int:not_id>/' , mark_notification_as_read , name= "mark_notification_as_read"),
    path('auto_complete' , auto_complete , name='auto_complete'),
    
]


def custom_404(request , exception):
    return render(request ,"blog/404.html" , status=404)


