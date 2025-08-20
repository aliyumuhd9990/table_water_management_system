from django.urls import path
from .views import *


app_name='product'


urlpatterns = [
    path('product_list/', ProductListView, name= 'product_list'),
    path('<int:id>/', ProductDetailView, name= 'product_detail'),
]
