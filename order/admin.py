from django.contrib import admin
from .models import *


# Register your models here.
# Register your models here.   
class OrderItemInLine(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['email', 'full_name', 'phone', 'status', 'paid']

    list_filter = ['created_at', 'paid']
    inlines = [OrderItemInLine]
    
admin.site.register(DriverRoute)