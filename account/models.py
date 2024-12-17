from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL , on_delete=models.CASCADE)
    age = models.IntegerField(blank=True , null=True)
    image = models.ImageField(upload_to="user/%Y/%m/%d" , blank=True)

    def __str__(self):
        return f'profile of {self.user.username}'
    


class Follow(models.Model):
    follower = models.ForeignKey(User , related_name="Following" , on_delete=models.CASCADE)
    author = models.ForeignKey(User , related_name="follwers" , on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('follower' , 'author')

    def __str__(self):
        return f"{self.follower} follows {self.author}"
    
