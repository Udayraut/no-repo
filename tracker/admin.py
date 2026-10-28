from django.contrib import admin
from .models import SocialPost, PostMetric, DailyLog


class PostMetricInline(admin.TabularInline):
    model = PostMetric
    extra = 1


@admin.register(SocialPost)
class SocialPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'platform', 'post_type', 'status', 'scheduled_at', 'published_at', 'created_at')
    list_filter = ('platform', 'status', 'post_type')
    search_fields = ('title', 'caption', 'tags', 'user__username')
    inlines = [PostMetricInline]


@admin.register(PostMetric)
class PostMetricAdmin(admin.ModelAdmin):
    list_display = ('post', 'metric_date', 'source', 'views', 'likes', 'comments', 'shares', 'reach')
    list_filter = ('source', 'metric_date')
    search_fields = ('post__title', 'notes')


@admin.register(DailyLog)
class DailyLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'log_date', 'focus_area', 'content_items_created', 'hours_spent', 'productivity_score')
    list_filter = ('productivity_score', 'log_date')
    search_fields = ('user__username', 'focus_area', 'key_learnings')
