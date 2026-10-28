from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('organization_name', models.CharField(blank=True, default='', max_length=120)),
                ('bio', models.TextField(blank=True, default='', max_length=500)),
                ('job_title', models.CharField(blank=True, default='', max_length=100)),
                ('timezone', models.CharField(choices=[('UTC', 'UTC (Coordinated Universal Time)'), ('America/New_York', 'Eastern Time (US & Canada)'), ('America/Chicago', 'Central Time (US & Canada)'), ('America/Denver', 'Mountain Time (US & Canada)'), ('America/Los_Angeles', 'Pacific Time (US & Canada)'), ('Europe/London', 'London (GMT)'), ('Europe/Paris', 'Paris (CET)'), ('Asia/Kolkata', 'India (IST)'), ('Asia/Tokyo', 'Tokyo (JST)'), ('Australia/Sydney', 'Sydney (AEST)')], default='UTC', max_length=50)),
                ('website', models.URLField(blank=True, default='')),
                ('avatar_url', models.URLField(blank=True, default='', max_length=500)),
                ('email_notifications', models.BooleanField(default=True, help_text='Receive goal and milestone alerts via email')),
                ('weekly_digest', models.BooleanField(default=True, help_text='Receive weekly summary report')),
                ('notify_on_deadline', models.BooleanField(default=True, help_text='Alert 24 hours before goal deadline')),
                ('is_premium', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
