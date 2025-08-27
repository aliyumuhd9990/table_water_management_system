from accounts.models import StaffGroup, CustomUser

def assign_driver_to_order(order):
    try:
        group_a = StaffGroup.objects.get(name="A")  # Drivers group
        drivers = group_a.members.all()

        if not drivers.exists():
            return None  # No driver available

        # Strategy: pick the driver with the fewest active deliveries
        driver = min(
            drivers,
            key=lambda d: d.deliveries.filter(status__in=["assigned", "delivering"]).count()
        )

        order.driver = driver
        order.status = "assigned"
        order.save()
        return driver
    except StaffGroup.DoesNotExist:
        return None
