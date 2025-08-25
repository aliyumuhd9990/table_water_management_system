from django.shortcuts import render, redirect
from .models import Notification

app_name = 'notifications'

def notification_list(request):
    notifications = Notification.objects.filter(user=request.user).order_by("-created_at")
    
    context = {
        'header_name': 'Notification Page',
        "notifications": notifications,
    }
    return render(request, "notifications/list.html", context)

def mark_as_read(request, pk):
    notif = Notification.objects.get(pk=pk, user=request.user)
    notif.is_read = True
    notif.save()
    return redirect("notifications:list")
