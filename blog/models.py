from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils import timezone
from PIL import Image

def validate_image_dimensions(image):
    min_width = 800
    min_height = 300

    with Image.open(image) as img:
        width, height = img.size

    if width <= min_width or height <= min_height:
        raise ValidationError(f"Image must be exactly {min_width}x{min_height} pixels.")


class BasePage(models.Model):
    title = models.CharField(max_length=150)
    sub_title = models.CharField(max_length=255)
    bg_image = models.ImageField(upload_to="images/%Y/%m/%d",validators=[validate_image_dimensions])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract= True

    def __str__(self):
        return self.title

class HomePage(BasePage):
   pass

class AboutPage(BasePage):
    description = models.TextField()

class ContactPage(BasePage):
    description = models.TextField()



class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = ("DF" , "Draft")
        PUBLISHED = ("PB" , "Published")

    title = models.CharField(max_length=255)
    author = models.ForeignKey(User , on_delete=models.CASCADE)
    slug = models.SlugField(max_length=255)
    body = models.TextField()
    bg_image = models.ImageField(upload_to="images/%Y/%m/%d/header_images" , blank=True)
    post_image = models.ImageField(upload_to="images/%Y/%m/%d/post_images", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    publish = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=2, choices=Status.choices , default=Status.PUBLISHED)
    views = models.PositiveBigIntegerField(default=0)
    likes = models.ManyToManyField(User , related_name="post_likes" , blank=True)


    class Meta:
        ordering = ['-publish']

        indexes = [
            models.Index(fields=['-publish'])
        ]

    def get_absolute_url(self):
        return reverse("post_details", args=[
            self.slug,
        ])
    
    def likes_count(self):
        return self.likes.count()

    def __str__(self):
        return self.title
    


class Comment(models.Model):
    post = models.ForeignKey(Post , on_delete=models.CASCADE , related_name="comments_post")
    user = models.ForeignKey(User , on_delete=models.CASCADE , related_name="comments_user")
    body = models.TextField()
    email = models.EmailField(blank=True , null=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"comment by {self.user} for {self.post}"
    


class Notification(models.Model):
    
    NOTIFICATION_TYPES = [
        ('COMMENT', 'comment'),
        ('LIKE' , 'like'),
        ('FOLLOW' , 'follow'),
        ('NEW_POST','new_post'),
    ]
    user = models.ForeignKey(User , on_delete=models.CASCADE , related_name='notifications')
    type = models.CharField(max_length=255 , choices=NOTIFICATION_TYPES , default='OTHER')
    link = models.URLField(blank=True, null=True)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username} : {self.type}"
    

    
