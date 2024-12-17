from django.contrib import admin
from .models import  AboutPage , ContactPage , HomePage , Post , Comment , Notification


admin.site.register(HomePage)
admin.site.register(AboutPage)
admin.site.register(ContactPage)
admin.site.register(Comment)
admin.site.register(Notification)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title' , 'author' , 'slug' , 'created_at' , 'status']
    list_filter = ['status' , 'created_at' , 'publish' , 'author']
    search_fields = ['body' , 'title']
    prepopulated_fields = { 'slug' : ('title',)}
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    ordering = ['status' , 'publish']





