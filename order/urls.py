from django.urls import path
from .views import *

urlpatterns = [
    path('create/', CreateOrderView, name='create_order'),
    path('success/<int:order_id>/', OrderSuccessView, name='order_success'),
    path('order_history/', OrderListView, name='order_list'),
     path("pending_orders/", PendingOrdersView, name="pending_orders"),
    path('invoice/<int:invoice_id>/', InvoiceView, name='invoice'),

]
