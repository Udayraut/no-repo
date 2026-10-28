from .models import Notification


def unread_notifications_count(request):
    """
    Context processor providing unread notifications count globally to templates.
    """
    if request.user.is_authenticated:
        count = Notification.objects.filter(user=request.user, is_read=False).count()
        return {'unread_notifications_count': count}
    return {'unread_notifications_count': 0}
