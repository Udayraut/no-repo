from decimal import Decimal
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
            name='GrowthGoal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Goal description (e.g. 100k Monthly Video Views)', max_length=200)),
                ('metric_type', models.CharField(choices=[('views', 'Total Views'), ('engagement_rate', 'Engagement Rate (%)'), ('playstore_installs', 'Play Store Installs'), ('content_output', 'Content Pieces Published'), ('subscribers', 'Followers / Subscribers')], default='views', max_length=30)),
                ('target_value', models.DecimalField(decimal_places=2, help_text='Numerical goal target', max_digits=12)),
                ('current_value', models.DecimalField(decimal_places=2, default=Decimal('0.00'), help_text='Current observed value', max_digits=12)),
                ('unit', models.CharField(blank=True, default='', help_text='e.g. views, installs, %, posts', max_length=20)),
                ('start_date', models.DateField(default=django.utils.timezone.now)),
                ('deadline', models.DateField(help_text='Target deadline date')),
                ('status', models.CharField(choices=[('active', 'In Progress'), ('completed', 'Completed'), ('paused', 'Paused'), ('missed', 'Missed')], default='active', max_length=15)),
                ('notes', models.TextField(blank=True, default='')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='growth_goals', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['deadline', '-created_at'],
            },
        ),
        migrations.CreateModel(
            name='PlayStoreMetric',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_name', models.CharField(default='Skyniya App', max_length=150)),
                ('package_name', models.CharField(default='com.skyniya.app', max_length=200)),
                ('metric_date', models.DateField(default=django.utils.timezone.now)),
                ('source', models.CharField(choices=[('MANUAL', 'Manual Entry'), ('API_SYNC', 'Google Play API Sync')], default='MANUAL', help_text='Identifies manual vs API synchronized metric sources', max_length=15)),
                ('store_listing_visitors', models.PositiveIntegerField(default=0, help_text='Unique visitors who viewed your store listing')),
                ('store_listing_acquisitions', models.PositiveIntegerField(default=0, help_text='New first-time downloads / installs from listing')),
                ('uninstalls', models.PositiveIntegerField(default=0, help_text='Number of user uninstalls')),
                ('active_devices', models.PositiveIntegerField(default=0, help_text='Devices currently retaining the app')),
                ('average_rating', models.DecimalField(decimal_places=2, default=Decimal('4.50'), help_text='Average store rating (1.00 - 5.00)', max_digits=3)),
                ('notes', models.TextField(blank=True, default='', help_text='Campaign context or ASO test notes')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='playstore_metrics', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-metric_date', '-created_at'],
                'unique_together': {('user', 'package_name', 'metric_date', 'source')},
            },
        ),
    ]
