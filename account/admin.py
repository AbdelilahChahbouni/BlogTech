from django.contrib import admin
from .models import Profile , Follow


@admin.register(Profile)
class PrfileAdmin(admin.ModelAdmin):
    list_display = ['user' , 'age' , 'image']
    raw_id_fields = ['user',]


admin.site.register(Follow)