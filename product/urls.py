from django.urls import path
from .views import *


app_name='product'


urlpatterns = [
    path('<int:id>/', ProductDetailView, name= 'product_detail')
]
