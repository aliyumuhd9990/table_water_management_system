from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from .managers import CustomUserManager
from django.urls import reverse


class CustomUser(AbstractBaseUser, PermissionsMixin):
    full_name = models.CharField(max_length=30, blank=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Other required fields apart from email

    def __str__(self):
        return self.email


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
  