from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse


class SocialPost(models.Model):
    PLATFORM_CHOICES = [
        ('instagram', 'Instagram'),
        ('youtube', 'YouTube'),
        ('twitter', 'Twitter / X'),
        ('tiktok', 'TikTok'),
        ('linkedin', 'LinkedIn'),
        ('facebook', 'Facebook'),
    ]

    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('scheduled', 'Scheduled'),
        ('published', 'Published'),
    ]

    TYPE_CHOICES = [
        ('reel_short', 'Reel / Short / Clip'),
        ('image_post', 'Single Image'),
        ('carousel', 'Carousel Slider'),
        ('text_thread', 'Text Thread'),
        ('long_video', 'Long-form Video'),
        ('article', 'Newsletter / Article'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=200, help_text="Internal working title or headline")
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    post_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='reel_short')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    caption = models.TextField(help_text="Full post caption, script, or copy")
    tags = models.CharField(max_length=250, blank=True, help_text="Comma-separated hashtags or keywords")
    scheduled_at = models.DateTimeField(null=True, blank=True, help_text="Planned release date and time")
    published_at = models.DateTimeField(null=True, blank=True, help_text="Actual release date and time")
    post_url = models.URLField(max_length=500, blank=True, help_text="Direct link to live post")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.get_platform_display()}] {self.title}"

    def get_absolute_url(self):
        return reverse('tracker:post_detail', kwargs={'pk': self.pk})

    @property
    def latest_metric(self):
        return self.metrics.order_by('-metric_date', '-created_at').first()

    @property
    def total_views(self):
        latest = self.latest_metric
        return latest.views if latest else 0

    @property
    def total_engagement(self):
        latest = self.latest_metric
        return latest.total_engagement if latest else 0


class PostMetric(models.Model):
    SOURCE_CHOICES = [
        ('MANUAL', 'Manual Entry'),
        ('API_SYNC', 'API Synchronized'),
    ]

    post = models.ForeignKey(SocialPost, on_delete=models.CASCADE, related_name='metrics')
    metric_date = models.DateField(default=timezone.now, help_text="Date for which these metrics apply")
    source = models.CharField(
        max_length=15, 
        choices=SOURCE_CHOICES, 
        default='MANUAL',
        help_text="Identifies whether this metric snapshot was manually recorded or API-fetched"
    )
    views = models.PositiveIntegerField(default=0, help_text="Video views or impressions count")
    likes = models.PositiveIntegerField(default=0)
    comments = models.PositiveIntegerField(default=0)
    shares = models.PositiveIntegerField(default=0)
    saves = models.PositiveIntegerField(default=0)
    clicks = models.PositiveIntegerField(default=0)
    reach = models.PositiveIntegerField(default=0)
    impressions = models.PositiveIntegerField(default=0)
    notes = models.TextField(blank=True, default='', help_text="Performance observation or campaign context")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-metric_date', '-created_at']
        unique_together = ('post', 'metric_date', 'source')

    def __str__(self):
        return f"{self.post.title} Metrics ({self.metric_date}) - {self.source}"

    @property
    def total_engagement(self):
        return self.likes + self.comments + self.shares + self.saves + self.clicks

    @property
    def engagement_rate(self):
        base = self.views if self.views > 0 else self.impressions
        if base > 0:
            return round((self.total_engagement / base) * 100, 2)
        return 0.0


class DailyLog(models.Model):
    """
    Daily content creation log and productivity tracker.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='daily_logs')
    log_date = models.DateField(default=timezone.now)
    focus_area = models.CharField(max_length=150, help_text="Main objective (e.g. YouTube Scripting, TikTok Reels)")
    content_items_created = models.PositiveIntegerField(default=1, help_text="Number of assets or posts finalized")
    hours_spent = models.DecimalField(max_digits=4, decimal_places=1, default=2.0, help_text="Focused hours dedicated today")
    productivity_score = models.PositiveSmallIntegerField(
        default=5, 
        help_text="Productivity rating on a scale from 1 (lowest) to 5 (highest)"
    )
    key_learnings = models.TextField(blank=True, default='', help_text="What worked, what flopped, algorithm shifts")
    notes = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-log_date']
        unique_together = ('user', 'log_date')

    def __str__(self):
        return f"{self.user.username} Daily Log - {self.log_date}"
