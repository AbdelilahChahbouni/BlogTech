from django.shortcuts import render, get_object_or_404 , redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.text import slugify
from .models import *
from .forms import CommentForm ,ContactForm , PostForm , PostUpdateForm
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required 
from django.db.models import Q
import json




def default(request):
    return render(request, "blog/default.html",{})


@login_required
def home(request):
    page = HomePage.objects.all()[0]
    query = request.POST.get("q")
    if query:
        posts = Post.objects.filter(
            Q(title__icontains=query) | Q(body__icontains=query),
            status=Post.Status.PUBLISHED
        )
    else:
        posts = Post.objects.filter(status="PB")
    paginator = Paginator(posts , 5)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'blog/home.html', {"page":page , 'page_obj':page_obj})

def auto_complete(request):
    if "term" in request.GET :
        pf = Post.objects.filter(title__istartswith=request.GET.get("term"))
        titles = list()
        for post in pf:
            titles.append(post.title)
        return JsonResponse(titles , safe=False)
    return JsonResponse({'message':"error in response"})


def about(request):
    page = AboutPage.objects.all()[0]
    return render(request , 'blog/about.html', {"page":page})


def contact(request):
    page = ContactPage.objects.all()[0]
    return render(request , 'blog/contact.html',{"page":page})

@login_required
def author_posts(request):
    author_posts = Post.objects.filter(author= request.user)
    return render(request , "blog/author_posts.html" , {'author_posts':author_posts})

@login_required
def post_details(request , post):
    post = get_object_or_404(Post , slug=post )
    post.views += 1
    post.save(update_fields=['views']) 
    comments = Comment.objects.filter(post=post)
    return render(request , "blog/post_details.html",{'post':post , 'comments':comments})

@login_required
def create_post(request):
    if request.method == 'POST':
        print("post")
        form_post = PostForm(data=request.POST ,files=request.FILES)
        if form_post.is_valid():
            print("valid")
            new_form = form_post.save(commit=False)
            new_form.author = request.user
            new_form.slug = slugify(new_form.title)
            new_form.save()
            return redirect("home")
    else:
        print("not post")
        form_post = PostForm()  
    return render(request,'blog/create_post.html', {'form_post':form_post})



@login_required
def update_post(request , post_id):
    post = get_object_or_404(Post , id = post_id)
    if request.method == "POST":
        form = PostUpdateForm(instance=post , data=request.POST , files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request , "the post updated successfully")
            return redirect('author_posts')
        else:
            messages.error(request,"the updated error ")
    else:
        form = PostUpdateForm(instance=post)
    return render(request,"blog/update_post.html" , {'form':form})



@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post , id=post_id)
    if request.method == "POST":
        post.delete()
        return redirect("author_posts")
    return render(request , 'blog/delete_post.html' , {'post':post})

# @login_required
# def post_comment(request , post_id):
#     post = get_object_or_404(Post , id=post_id)
#     comments = Comment.objects.filter(post=post)
#     if request.method == "POST":
#         form = CommentForm(data=request.POST)
#         if form.is_valid():
#             print("valid")
#             comment = form.save(commit=False)
#             comment.post = post
#             comment.user = request.user
#             comment.save()
#             comments = Comment.objects.filter(post=post)
#     else:
#         form = CommentForm()

#     return render(request , "blog/post_details.html" , {'comments':comments , 'form':form , 'post':post } )

@login_required
def post_comment(request):
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        post_id = request.POST.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        user = request.user
        body = request.POST.get('body')
        if body:
            comment = Comment.objects.create(post=post, user=user, body=body)
            return JsonResponse({
                "success": True,
                "username": comment.user.username,
                "created_at": comment.created_at.strftime("%B %d, %Y, %I:%M %p"),
                "body": comment.body,
                "profile_image_url": comment.user.profile.image.url if comment.user.profile.image else ""
            })

    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)




# from django.http import JsonResponse
# from django.contrib.auth.decorators import login_required
# from .models import Post

# @login_required
# def post_like(request, post_id):
#     post = Post.objects.get(id=post_id)
    
#     if request.user in post.likes.all():
#         post.likes.remove(request.user)
#         liked = False
#     else:
#         post.likes.add(request.user)
#         liked = True

#     # Update the like count
#     likes_count = post.likes.count()

#     response_data = {
#         'likes_count': likes_count,
#         'user_liked': liked,
#     }

#     return JsonResponse(response_data)



# def post_like(request , post_id):
#     post = get_object_or_404(Post , id=post_id)
    
#     if request.user in post.likes.all():
#         post.likes.remove(request.user)
#     else:
#         post.likes.add(request.user)
#     return redirect("post_details" , post = post.slug)


@login_required
def post_like(request):
    if request.method =="POST":
        post_id = request.POST.get('post_id')
        post = get_object_or_404(Post , id = post_id )
        if post.likes.filter(id = request.user.id).exists():
            post.likes.remove(request.user)
            liked = False
        else:
            post.likes.add(request.user)
            liked = True
        return JsonResponse({"liked":liked , "likes_count": post.likes_count()})
    return JsonResponse({'error': 'Invalid request'}, status=400)


def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            subject = f"New Contact Form Submission from {name}"
            email_message = f"Name: {name}\nEmail: {email}\nMessage:\n{message}"
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [email]

            send_mail(subject, email_message , from_email , recipient_list )

            messages.success(request , "your message has been sent successfully ")

            redirect("contact")

    else:
        form = ContactForm()

    return render(request, "blog/contact.html" , {'form':form})



def mark_notification_as_read(request , not_id):
    notification = get_object_or_404(Notification , id=not_id , user=request.user)
    notification.is_read = True
    notification.save()
    return redirect(notification.link)


