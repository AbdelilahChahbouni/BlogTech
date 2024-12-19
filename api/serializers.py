from rest_framework import serializers
from blog.models import Post ,  Comment


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'id', 'title', 'author', 'body', 'created_at', 'updated_at',
            'publish', 'status', 'bg_image', 'post_image', 'likes', 'views'
        ]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['post' , 'user' , 'body' , 'created_at' , 'updated_at' , 'is_active' , 'email']