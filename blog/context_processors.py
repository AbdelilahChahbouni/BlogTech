from django.contrib.auth.models import AnonymousUser

def notifications_count(request):
    # Ensure the user is authenticated
    if isinstance(request.user, AnonymousUser):
        return {'unread_notifications_count': 0}
    
    unread_notifications = request.user.notifications.filter(is_read=False).count()
    return {'unread_notifications_count': unread_notifications}
