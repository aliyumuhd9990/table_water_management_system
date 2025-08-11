from django.contrib import admin
from.models import *
from django.contrib.auth.models import Group, User
from django.contrib.admin.sites import NotRegistered

# Register your models here.
admin.site.unregister(Group)
try:
    admin.site.unregister(User)
except NotRegistered:
    pass  # Or log the info if needed

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = [
        'email', 'full_name', 'last_login', 
    ]

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'profile_img', 'contact'
    ]
