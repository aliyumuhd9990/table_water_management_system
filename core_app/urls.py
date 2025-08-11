from django.urls import path
from .views import *


app_name = 'core_app'
urlpatterns = [
    path('', IndexView, name='index'),
]