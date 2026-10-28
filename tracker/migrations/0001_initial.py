from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SocialPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Internal working title or headline', max_length=200)),
                ('platform', models.CharField(choices=[('instagram', 'Instagram'), ('youtube', 'YouTube'), ('twitter', 'Twitter / X'), ('tiktok', 'TikTok'), ('linkedin', 'LinkedIn'), ('facebook', 'Facebook')], max_length=20)),
                ('post_type', models.CharField(choices=[('reel_short', 'Reel / Short / Clip'), ('image_post', 'Single Image'), ('carousel', 'Carousel Slider'), ('text_thread', 'Text Thread'), ('long_video', 'Long-form Video'), ('article', 'Newsletter / Article')], default='reel_short', max_length=20)),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('scheduled', 'Scheduled'), ('published', 'Published')], default='draft', max_length=20)),
                ('caption', models.TextField(help_text='Full post caption, script, or copy')),
                ('tags', models.CharField(blank=True, help_text='Comma-separated hashtags or keywords', max_length=250)),
                ('scheduled_at', models.DateTimeField(blank=True, help_text='Planned release date and time', null=True)),
                ('published_at', models.DateTimeField(blank=True, help_text='Actual release date and time', null=True)),
                ('post_url', models.URLField(blank=True, help_text='Direct link to live post', max_length=500)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='DailyLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('log_date', models.DateField(default=django.utils.timezone.now)),
                ('focus_area', models.CharField(help_text='Main objective (e.g. YouTube Scripting, TikTok Reels)', max_length=150)),
                ('content_items_created', models.PositiveIntegerField(default=1, help_text='Number of assets or posts finalized')),
                ('hours_spent', models.DecimalField(decimal_places=1, default=2.0, help_text='Focused hours dedicated today', max_digits=4)),
                ('productivity_score', models.PositiveSmallIntegerField(default=5, help_text='Productivity rating on a scale from 1 (lowest) to 5 (highest)')),
                ('key_learnings', models.TextField(blank=True, default='', help_text='What worked, what flopped, algorithm shifts')),
                ('notes', models.TextField(blank=True, default='')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='daily_logs', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-log_date'],
                'unique_together': {('user', 'log_date')},
            },
        ),
        migrations.CreateModel(
            name='PostMetric',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('metric_date', models.DateField(default=django.utils.timezone.now, help_text='Date for which these metrics apply')),
                ('source', models.CharField(choices=[('MANUAL', 'Manual Entry'), ('API_SYNC', 'API Synchronized')], default='MANUAL', help_text='Identifies whether this metric snapshot was manually recorded or API-fetched', max_length=15)),
                ('views', models.PositiveIntegerField(default=0, help_text='Video views or impressions count')),
                ('likes', models.PositiveIntegerField(default=0)),
                ('comments', models.PositiveIntegerField(default=0)),
                ('shares', models.PositiveIntegerField(default=0)),
                ('saves', models.PositiveIntegerField(default=0)),
                ('clicks', models.PositiveIntegerField(default=0)),
                ('reach', models.PositiveIntegerField(default=0)),
                ('impressions', models.PositiveIntegerField(default=0)),
                ('notes', models.TextField(blank=True, default='', help_text='Performance observation or campaign context')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='metrics', to='tracker.socialpost')),
            ],
            options={
                'ordering': ['-metric_date', '-created_at'],
                'unique_together': {('post', 'metric_date', 'source')},
            },
        ),
    ]
