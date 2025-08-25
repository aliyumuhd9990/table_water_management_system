from django.urls import path
from . import views

app_name = "notifications"

urlpatterns = [
    path("", views.notification_list, name="list"),
    path("<int:pk>/read/", views.mark_as_read, name="mark_as_read"),
    path("<int:pk>/delete/", views.delete_notification, name="delete"),
    path("clear/", views.clear_all_notifications, name="clear_all"),
]
