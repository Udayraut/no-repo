from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal


class PlayStoreMetric(models.Model):
    """
    Tracks Google Play Store visitor and install metrics.
    Clearly distinguishes manual entries from API synchronized metrics.
    """
    SOURCE_CHOICES = [
        ('MANUAL', 'Manual Entry'),
        ('API_SYNC', 'Google Play API Sync'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='playstore_metrics')
    app_name = models.CharField(max_length=150, default='Skyniya App')
    package_name = models.CharField(max_length=200, default='com.skyniya.app')
    metric_date = models.DateField(default=timezone.now)
    source = models.CharField(
        max_length=15, 
        choices=SOURCE_CHOICES, 
        default='MANUAL',
        help_text="Identifies manual vs API synchronized metric sources"
    )
    store_listing_visitors = models.PositiveIntegerField(
        default=0, 
        help_text="Unique visitors who viewed your store listing"
    )
    store_listing_acquisitions = models.PositiveIntegerField(
        default=0, 
        help_text="New first-time downloads / installs from listing"
    )
    uninstalls = models.PositiveIntegerField(default=0, help_text="Number of user uninstalls")
    active_devices = models.PositiveIntegerField(default=0, help_text="Devices currently retaining the app")
    average_rating = models.DecimalField(
        max_digits=3, 
        decimal_places=2, 
        default=Decimal('4.50'), 
        help_text="Average store rating (1.00 - 5.00)"
    )
    notes = models.TextField(blank=True, default='', help_text="Campaign context or ASO test notes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-metric_date', '-created_at']
        unique_together = ('user', 'package_name', 'metric_date', 'source')

    def __str__(self):
        return f"{self.app_name} ({self.metric_date}) - {self.source}"

    @property
    def conversion_rate(self):
        if self.store_listing_visitors > 0:
            return round((self.store_listing_acquisitions / self.store_listing_visitors) * 100, 2)
        return 0.0

    @property
    def net_installs(self):
        return max(0, self.store_listing_acquisitions - self.uninstalls)


class GrowthGoal(models.Model):
    """
    Configurable SaaS growth target with deadline and progress tracking.
    """
    METRIC_TYPE_CHOICES = [
        ('views', 'Total Views'),
        ('engagement_rate', 'Engagement Rate (%)'),
        ('playstore_installs', 'Play Store Installs'),
        ('content_output', 'Content Pieces Published'),
        ('subscribers', 'Followers / Subscribers'),
    ]

    STATUS_CHOICES = [
        ('active', 'In Progress'),
        ('completed', 'Completed'),
        ('paused', 'Paused'),
        ('missed', 'Missed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='growth_goals')
    title = models.CharField(max_length=200, help_text="Goal description (e.g. 100k Monthly Video Views)")
    metric_type = models.CharField(max_length=30, choices=METRIC_TYPE_CHOICES, default='views')
    target_value = models.DecimalField(max_digits=12, decimal_places=2, help_text="Numerical goal target")
    current_value = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'), help_text="Current observed value")
    unit = models.CharField(max_length=20, default='', blank=True, help_text="e.g. views, installs, %, posts")
    start_date = models.DateField(default=timezone.now)
    deadline = models.DateField(help_text="Target deadline date")
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='active')
    notes = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['deadline', '-created_at']

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"

    @property
    def progress_percentage(self):
        if self.target_value <= 0:
            return 0
        perc = (self.current_value / self.target_value) * Decimal('100.0')
        return min(100.0, round(float(perc), 1))

    @property
    def days_remaining(self):
        today = timezone.now().date()
        diff = (self.deadline - today).days
        return diff

    @property
    def is_overdue(self):
        return self.status == 'active' and self.days_remaining < 0
