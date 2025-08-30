from .models import *
from django.db.models import Q
from django.utils import timezone
# from django.db.models import Count

def pending_orders_count(request):
    if request.user.is_authenticated:
        count = Order.objects.filter(
            user=request.user
        ).filter(
            Q(status="pending") or Q(status="processing")
        ).count()
    else:
        count = 0
    return {
        "pending_orders_count": count
    }


# def get_driver_for_lga(lga):
#     drivers = DriverRoute.objects.filter(lga=lga).annotate(order_count=Count("driver__deliveries"))
#     return drivers.order_by("order_count").first().driver if drivers.exists() else None


def driver_delivery_counts(request):
    context = {}
    if request.user.is_authenticated and hasattr(request.user, "role") and request.user.role == "staff":
        driver = request.user

        today = timezone.now().date()
        month_start = today.replace(day=1)

        # Counts by status
        assigned = Order.objects.filter(driver=driver, status="assigned").count()
        delivering = Order.objects.filter(driver=driver, status="delivering").count()
        delivered = Order.objects.filter(driver=driver, status="delivered").count()

        # Totals
        total = assigned + delivering + delivered

        # ✅ Daily delivered count
        delivered_today = Order.objects.filter(
            driver=driver,
            status="delivered",
            created_at__date=today
        ).count()

        # ✅ Monthly delivered count
        delivered_this_month = Order.objects.filter(
            driver=driver,
            status="delivered",
            created_at__date__gte=month_start
        ).count()

        context.update({
            "assigned_orders_count": assigned,
            "delivering_orders_count": delivering,
            "delivered_orders_count": delivered,
            "total_orders_count": total,
            "delivered_today": delivered_today,
            "delivered_this_month": delivered_this_month,
        })

    return context