"""Admin registration for custom user."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class BeyondCVUserAdmin(UserAdmin):
    """Expose application role in Django admin."""

    fieldsets = UserAdmin.fieldsets + (("BeyondCV", {"fields": ("role",)}),)
    list_display = ("email", "username", "role", "is_staff", "is_active")
