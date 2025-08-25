from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('core_app.urls', namespace='core_app')),
    path('admin/', admin.site.urls),
    path('account/', include('accounts.urls')),
    path('cart/', include('cart.urls')),
    path('product/', include('product.urls', namespace='product')),
    path('payment/', include('payment.urls', namespace='payment')),
    path('notifications/', include('notifications.urls', namespace='notifications')),
    path('orders/', include('order.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

