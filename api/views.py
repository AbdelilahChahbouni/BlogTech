from django.shortcuts import render , get_object_or_404
from rest_framework.pagination import PageNumberPagination
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate , login , logout
from django.utils.crypto import get_random_string
from .models import ResetPasswordToken
from django.core.mail import send_mail


@api_view(['GET' , 'POST'])
def post_list_create_api(request):
    if request.method == "GET":
        posts = Post.objects.filter(status="PB").order_by("-publish")
        paginator = PageNumberPagination()
        paginator.page_size = 1
        result_page = paginator.paginate_queryset(posts , request)
        serializer = PostSerializer(result_page , many=True)
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



@api_view(['POST'])
def register(request):
    print("hello")
    serializer = RegisterSerializer(data = request.data)
    if serializer.is_valid():
        user = serializer.save()
        Profile.objects.create(user=user)
        return Response({"message":"User Created Successfully"} , status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def show_profile(request, user_id):
    try:
        user_profile = Profile.objects.get(user = user_id)
        profile_serializer = ProfileSerializer(user_profile)
        user_serializer = UserSerializer(user_profile.user)
        data_response = {
            "user" : user_serializer.data,
            "profile" : profile_serializer.data
        }
        return Response(data_response , status=status.HTTP_202_ACCEPTED)
    except Profile.DoesNotExist:
        return Response('error Profile Not Found' , status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def edite_profile(request , profile_id):
    try:
        user_profile = Profile.objects.get(user = profile_id)
        profile_serializer = ProfileSerializer(user_profile ,data= request.data , partial=True)
        user_serializer = UserSerializer(user_profile.user , data = request.data , partial=True)
        if profile_serializer.is_valid() and user_serializer.is_valid():
            user_serializer.save()
            profile_serializer.save()
            return Response({'message': "The profile was updated successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"message":"the data is not valid"}, status=status.HTTP_400_BAD_REQUEST)

    except Profile.DoesNotExist:
        return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def login_api(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({"error":"please provide both username and password"})
    user = authenticate(request , username=username , password=password)
    if user is not None:
        login(request , user)
        return Response({"message":"Login Successfully"} , status=status.HTTP_200_OK)
    else:
        return Response({"error":"invalid Credentials"} , status=status.HTTP_401_UNAUTHORIZED)
    

@api_view(['POST'])
def logout_api(request):
    logout(request)
    return Response({"message":"Logout Successful"} , status=status.HTTP_200_OK)






@api_view(['POST'])
def reset_password(request):
    email = request.data.get('email')
    if not email:
        return Response({"error":"email is required"} , status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.get(email=email)
        code = get_random_string(32)
        ResetPasswordToken.objects.create(token=code , email=email)
        send_mail(
            'Password Reset Request',
            f'Use the following link to reset your password: http://localhost:8000/api/reset_password_confirm?token={code}',
            'dev4testemail@gmail.com',
            [email],
            fail_silently=False,
        )
        return Response({"message":"Link reset password sent to your email"}, status=status.HTTP_200_OK)

    except User.DoesNotExist:
        return Response({"error":"The User whit this email is dose not exists"} , status=status.HTTP_404_NOT_FOUND)
        

@api_view(['POST'])
def reset_password_confirm(request):
    token = request.GET.get('token')
    print(token)
    new_password = request.data.get("new_password")
    confirm_password = request.data.get('confirm_password')
    if new_password != confirm_password:
        return Response({"error":"the password and confirm password not the same" }, status=status.HTTP_400_BAD_REQUEST)
    try:
        token_obj = ResetPasswordToken.objects.get(token=token)
        user = User.objects.get(email=token_obj.email)
        user.set_password(new_password)
        user.save()
        token_obj.delete()
        return Response({"message":"Password Reset Successful"} , status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"error":"Invalid Token or the user not exists"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def list_notification(request):
    if request.method == "GET":
        nots = Notification.objects.filter(is_read=False )
        serializer = NotificationSerializer(nots , many=True)
        return Response(serializer.data)

    

@api_view(["PUT"])
def read_notification(request , id):
    if request.method == "PUT":
        noti =Notification.objects.get(id=id)
        noti.is_read = True
        noti.save()
        serializer = NotificationSerializer(noti)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    















