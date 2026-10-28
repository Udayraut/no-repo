from django.contrib import admin
from .models import PlayStoreMetric, GrowthGoal


@admin.register(PlayStoreMetric)
class PlayStoreMetricAdmin(admin.ModelAdmin):
    list_display = ('app_name', 'user', 'metric_date', 'source', 'store_listing_visitors', 'store_listing_acquisitions', 'average_rating')
    list_filter = ('source', 'metric_date', 'app_name')
    search_fields = ('app_name', 'package_name', 'notes')


@admin.register(GrowthGoal)
class GrowthGoalAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'metric_type', 'target_value', 'current_value', 'deadline', 'status')
    list_filter = ('status', 'metric_type', 'deadline')
    search_fields = ('title', 'notes')
