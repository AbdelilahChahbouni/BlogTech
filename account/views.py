from django.shortcuts import render , get_object_or_404 , redirect
from .forms import LoginForm , UserRegistrationForm , UserEditForm , ProfileEditForm
from django.contrib.auth.decorators import login_required
from .models import Profile , Follow
from blog.models import Post
from django.contrib import messages
from django.contrib.auth.models import User


def register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            print(user_form)
            new_user.name = new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            return render(request , "register_done.html" , {'user_form':user_form , 'new_user':new_user})
    else:
        user_form = UserRegistrationForm()

    return render(request , "register.html" , {'user_form':user_form})

@login_required
def edit_profile(request):
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile , data=request.POST , files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request , "the profile updated successfully")
        else:
            messages.error(request,"the updated error ")
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
       

    return render(request , "profile.html", {'user_form':user_form , 'profile_form':profile_form})



def show_profile(request , user_id):
    author = get_object_or_404(User , id=user_id)
    profile = author.profile
    author_posts = Post.objects.filter(author=author)
    is_following = False
    if request.user.is_authenticated:
        is_following = request.user.Following.filter(author=author).exists()

    return render(request , "show_profile.html" , 
                  {
                    'profile':profile , 
                    'author':author , 
                    'author_posts': author_posts ,
                    'is_following':is_following
                  }
                    )        


def follow_unfollow(request , author_id):
    author = get_object_or_404(User , id=author_id)
    if request.method == "POST":
        if request.user != author:
            action = request.POST.get("action")
            if action == "follow":
                Follow.objects.create(follower=request.user , author=author)
            elif action == "unfollow":
                Follow.objects.filter(follower=request.user , author=author).delete()
        
    return redirect("show_profile" , user_id = author.id)






