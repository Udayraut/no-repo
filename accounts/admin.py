from django.contrib import admin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'organization_name', 'timezone', 'is_premium', 'created_at')
    search_fields = ('user__username', 'user__email', 'organization_name')
    list_filter = ('timezone', 'is_premium', 'email_notifications')
