from django.shortcuts import render, redirect, get_object_or_404
from .models import Notification
from django.contrib.auth.decorators import login_required

app_name = 'notifications'


@login_required
def notification_list(request):
    notifications = Notification.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "notifications/list.html", {"notifications": notifications})

@login_required
def mark_as_read(request, pk):
    notif = get_object_or_404(Notification, pk=pk, user=request.user)
    notif.is_read = True
    notif.save()
    return redirect("notifications:list")

@login_required
def delete_notification(request, pk):
    notif = get_object_or_404(Notification, pk=pk, user=request.user)
    notif.delete()
    return redirect("notifications:list")

@login_required
def clear_all_notifications(request):
    Notification.objects.filter(user=request.user).delete()
    return redirect("notifications:list")
