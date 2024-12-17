from django.db.models.signals import post_save , m2m_changed , post_delete
from django.dispatch import receiver
from .models import Comment , Notification , Post
from account.models import Profile , Follow 
from django.contrib.auth.models import User 


@receiver(post_save, sender=Comment)
def create_comment_notification(sender , instance , created , **kwargs):
    if created:
        Notification.objects.create(
            user = instance.post.author,
            type = "COMMENT",
            message = f"{instance.user.username} Commented on your post {instance.post.title}",
            link = f"/post_details/{instance.post.slug}/"

        )

@receiver(post_save, sender=Follow)
def notify_follow(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user = instance.author,
            type="FOLLOW",
            message = f"{instance.follower.username} started following you ",
            link=f"/account/show_profile/{instance.follower.id}",
        )
        

@receiver(post_delete, sender=Follow)
def notify_unfollow(sender, instance, **kwargs):
    Notification.objects.create(
            user = instance.author,
            type="FOLLOW",
            message = f"{instance.follower.username} stopped following  you ",
            link=f"/account/show_profile/{instance.follower.id}"
        )


@receiver(post_save , sender=Post)
def create_post_notifiy(sender , instance , created , **kwargs):
    if created:
        author = instance.author
        followers = Follow.objects.filter(author=author)

        for follow in followers:
            Notification.objects.create(
            user = follow.follower,
            type = "NEW_POST",
            message = f"{author.username} create new post {instance.title}",
            link= f"/blog/post_details/{instance.slug}",
            )
