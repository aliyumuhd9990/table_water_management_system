from django.urls import path
from . import views

app_name = "reports"

urlpatterns = [
    path("my-reports/", views.staff_reports, name="my_reports"),
    path("add-report/", views.add_report, name="add_report"),
]
