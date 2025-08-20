from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from .managers import CustomUserManager
from django.urls import reverse


class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('customer', 'Customer'),
        ('staff', 'Staff'),
    )

    full_name = models.CharField(max_length=30, blank=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='customer')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Django’s built-in "staff" flag
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email} ({self.role})"


class Profile(models.Model):
    # user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='farmer_profile')
    email_token = models.CharField(max_length=200, default=False)
    is_verified = models.BooleanField(default=False)
    id_user = models.IntegerField()
    contact = models.CharField(max_length=11, default="080xxxxxx")
    bio = models.TextField(default="I'm New Here...............")
    profile_img = models.ImageField(upload_to='img/profile_images',  blank=True, null=False)

    def __self__(self):
        return self.user.email
  
class StaffGroup(models.Model):
    GROUP_CHOICES = (
        ('A', 'Group A'),
        ('B', 'Group B'),
        ('C', 'Group C'),
        ('D', 'Group D'),
    )

    name = models.CharField(max_length=1, choices=GROUP_CHOICES, unique=True)
    members = models.ManyToManyField(CustomUser, limit_choices_to={'role': 'staff'}, blank=True, related_name='staff_groups')

    def __str__(self):
        return f"Group {self.name}"