from django.db import models
from django.conf import settings
from product.models import Product
from accounts.models import CustomUser

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('assigned', 'Processing'),
        ('delivering', 'Out for Delivery'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )
    LGA_CHOICES = (
        ('tudun', 'Tudun Wada'),
        ('kumbotso', 'Kumbotso'),
        ('dambatta', 'Danbatta'),
        ('kiru', 'Kiru'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    driver = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name="deliveries", limit_choices_to={'role': 'staff'})
    lga = models.CharField(max_length=50,choices=LGA_CHOICES, default='kumbotso')  # selected during checkout

    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.TextField()
    address2 = models.TextField()
    phone = models.CharField(max_length=20)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        # ✅ Auto update status when paid is True
        if self.paid and self.status == "pending":
            self.status = "processing"
        super().save(*args, **kwargs)
   
    def __str__(self):
        return f"Order {self.id} by {self.user.email}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.pname}"
    
    
class DriverRoute(models.Model):
    lga = models.CharField(max_length=50, choices=Order.LGA_CHOICES)
    driver = models.ForeignKey(
        CustomUser, 
        on_delete=models.CASCADE, 
        limit_choices_to={'role': 'staff'},
        related_name="routes"
    )

    def __str__(self):
        return f"{self.driver.full_name} - {self.get_lga_display()}"