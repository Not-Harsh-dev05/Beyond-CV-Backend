"""Custom user model with explicit application roles."""

from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class BeyondCVUserManager(UserManager):
    """Ensure Django superusers receive the application administrator role."""

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("role", "ADMIN")
        return super().create_superuser(username, email, password, **extra_fields)


class User(AbstractUser):
    """BeyondCV user; public registration is always candidate-only."""

    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        RECRUITER = "RECRUITER", "Recruiter"
        CANDIDATE = "CANDIDATE", "Candidate"

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=16, choices=Role.choices, default=Role.CANDIDATE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    objects = BeyondCVUserManager()

    def save(self, *args, **kwargs):
        """Normalize email for unique account identity."""
        self.email = self.email.strip().lower()
        return super().save(*args, **kwargs)
