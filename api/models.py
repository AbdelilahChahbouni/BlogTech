from django.db import models

# Create your models here.
class ResetPasswordToken(models.Model):
    token= models.CharField(max_length=500)
    email = models.EmailField()

    def __str__(self):
        return self.email
    

    