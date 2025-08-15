from django.db import models
from django.urls import reverse 



# Create your models here.
class Product(models.Model):
    pname = models.CharField(max_length=30)
    pdesc = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    pimg = models.ImageField(upload_to='img/', height_field=None, width_field=None, max_length=100, default='img/water.jpg')
    
    def get_absolute_url(self):
        return reverse("product:product_detail", kwargs={"id": self.id})
    
