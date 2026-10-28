from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """
    Extends Django's User model with SaaS profile settings and preferences.
    """
    TIMEZONE_CHOICES = [
        ('UTC', 'UTC (Coordinated Universal Time)'),
        ('America/New_York', 'Eastern Time (US & Canada)'),
        ('America/Chicago', 'Central Time (US & Canada)'),
        ('America/Denver', 'Mountain Time (US & Canada)'),
        ('America/Los_Angeles', 'Pacific Time (US & Canada)'),
        ('Europe/London', 'London (GMT)'),
        ('Europe/Paris', 'Paris (CET)'),
        ('Asia/Kolkata', 'India (IST)'),
        ('Asia/Tokyo', 'Tokyo (JST)'),
        ('Australia/Sydney', 'Sydney (AEST)'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    organization_name = models.CharField(max_length=120, blank=True, default='')
    bio = models.TextField(max_length=500, blank=True, default='')
    job_title = models.CharField(max_length=100, blank=True, default='')
    timezone = models.CharField(max_length=50, choices=TIMEZONE_CHOICES, default='UTC')
    website = models.URLField(max_length=200, blank=True, default='')
    avatar_url = models.URLField(max_length=500, blank=True, default='')
    
    # Notification preferences
    email_notifications = models.BooleanField(default=True, help_text="Receive goal and milestone alerts via email")
    weekly_digest = models.BooleanField(default=True, help_text="Receive weekly summary report")
    notify_on_deadline = models.BooleanField(default=True, help_text="Alert 24 hours before goal deadline")

    # SaaS metadata
    is_premium = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} Profile"
