from django.shortcuts import render , get_object_or_404
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(['GET' , 'POST'])
def post_list_create_api(request):
    if request.method == "GET":
        posts = Post.objects.filter(status="PB").order_by("-publish")
        serializer = PostSerializer(posts , many=True)
        return Response(serializer.data)
    
    elif request.method == "POST":
        serializer = PostSerializer(data=request.data )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status=status.HTTP_201_CREATED)
    return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET' , 'PUT' , 'DELETE'])
def post_details_update_delete(request , pk):
    try:
        post = Post.objects.get(pk=pk , status="PB")
    except Post.DoesNotExist:
        return Response({'error': 'Post Not Found'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "GET":
        serializer = PostSerializer(post)
        return Response(serializer.data)
    elif request.method == "PUT":
        serializer = PostSerializer(post , data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def post_like(request ,pk):
    post = get_object_or_404(Post , id=pk)
    if post.likes.filter(id = request.user.id).exists():
        post.likes.remove(request.user)
        liked= False
    else:
        post.likes.add(request.user)
        liked = True
    return Response({'liked':liked , 'likes_count':post.likes_count()})


@api_view(['GET' , 'POST'])
def comment_list_create(request , post_id ):
    post = get_object_or_404(Post , id = post_id)
    if request.method == "GET":
        comments = post.comments_post
        # comments = Comment.objects.filter(post=post)
        print(comments)
        serializer = CommentSerializer(comments , many=True)
        return Response(serializer.data , status=status.HTTP_200_OK)
    elif request.method == "POST":
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(post = post , user = request.user)
            return Response({'message':'comment created'},serializer.data)
        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)












