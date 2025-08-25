from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order
from notifications.models import Notification

@receiver(post_save, sender=Order)
def order_status_notification(sender, instance, created, **kwargs):
    if not created:
        # Payment notification
        if instance.paid and instance.status == "processing":
            Notification.objects.create(
                user=instance.user,
                message=f"Your order #{instance.id} has been paid successfully and is now processing."
            )

        # Delivered notification
        if instance.status == "delivered":
            Notification.objects.create(
                user=instance.user,
                message=f"Your order #{instance.id} has been delivered. ✅"
            )

        # Cancelled notification
        if instance.status == "cancelled":
            Notification.objects.create(
                user=instance.user,
                message=f"Your order #{instance.id} was cancelled. ❌"
            )
