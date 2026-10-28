from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Notification


@login_required
def notification_list_view(request):
    """
    List user notifications with unread indicators and quick actions.
    """
    notifications = Notification.objects.filter(user=request.user)
    return render(request, 'notifications/list.html', {
        'notifications': notifications,
    })


@login_required
def mark_notification_read_view(request, pk):
    """
    Mark a specific notification as read and redirect to its link if available.
    """
    notif = get_object_or_404(Notification, pk=pk, user=request.user)
    notif.is_read = True
    notif.save()
    if notif.link_url:
        return redirect(notif.link_url)
    return redirect('notifications:list')


@login_required
def mark_all_notifications_read_view(request):
    """
    Mark all notifications for the current user as read.
    """
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    messages.success(request, "All notifications marked as read.")
    return redirect('notifications:list')


@login_required
def clear_notifications_view(request):
    """
    Delete all read notifications.
    """
    Notification.objects.filter(user=request.user, is_read=True).delete()
    messages.success(request, "Cleared read notifications.")
    return redirect('notifications:list')
