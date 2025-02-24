from django.contrib import admin
from .models import CustomUser, Package, Booking
from django.contrib.auth.admin import UserAdmin


# Register your models here.
from django.contrib import admin
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'is_staff', 'is_superuser')

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Package)
admin.site.register(Booking)
