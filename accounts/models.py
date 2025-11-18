from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom user manager for email-based authentication instead of username.
    """

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    """
    Custom user model that extends Django's AbstractUser.
    Allows for easy addition of custom fields in the future.
    """

    # Required fields
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    # Additional fields
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to="profile_pictures/", blank=True, null=True
    )

    # Subscription and storage fields
    PLAN_CHOICES = [
        ("free", "Free"),
        ("premium", "Premium"),
        ("pro", "Pro"),
    ]
    plan = models.CharField(
        max_length=10,
        choices=PLAN_CHOICES,
        default="free",
        help_text="User's subscription plan",
    )
    storage_limit = models.PositiveIntegerField(
        default=5, help_text="Storage limit in GB"
    )  # Default 5GB for free tier
    used_space = models.PositiveIntegerField(default=0, help_text="Used space in MB")

    email = models.EmailField(unique=True, db_index=True)  # Define email explicitly
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]  # Required for createsuperuser

    username = None  # Remove username since email is used instead

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    @property
    def available_space(self):
        """Return available space in MB"""
        return (self.storage_limit * 1024) - self.used_space

    def can_upload(self, file_size_mb):
        """Check if user can upload a file of given size in MB"""
        return self.available_space >= file_size_mb

    @property
    def plan_display(self):
        """Return the display name of the plan"""
        return dict(self.PLAN_CHOICES).get(self.plan, "Free")

    @property
    def storage_limit_mb(self):
        """Return storage limit in MB"""
        return self.storage_limit * 1024

    @property
    def used_space_percentage(self):
        """Return used space as percentage"""
        if self.storage_limit_mb == 0:
            return 0
        return (self.used_space / self.storage_limit_mb) * 100
