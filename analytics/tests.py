from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from decimal import Decimal
from .models import PlayStoreMetric, GrowthGoal


class AnalyticsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='analyticstester', email='analytics@skyniya.com', password='Password123!')
        self.client.force_login(self.user)

    def test_playstore_metric_calculations(self):
        metric = PlayStoreMetric.objects.create(
            user=self.user,
            app_name='Growth OS Mobile',
            package_name='com.skyniya.growth',
            metric_date=timezone.now().date(),
            source='MANUAL',
            store_listing_visitors=1000,
            store_listing_acquisitions=250,
            uninstalls=30,
            average_rating=Decimal('4.70')
        )
        self.assertEqual(metric.conversion_rate, 25.0)
        self.assertEqual(metric.net_installs, 220)

    def test_growth_goal_progress_and_completion(self):
        today = timezone.now().date()
        deadline = today + timezone.timedelta(days=14)
        goal = GrowthGoal.objects.create(
            user=self.user,
            title='Reach 1,000 Play Store Downloads',
            metric_type='playstore_installs',
            target_value=Decimal('1000.00'),
            current_value=Decimal('650.00'),
            start_date=today,
            deadline=deadline,
            status='active'
        )
        self.assertEqual(goal.progress_percentage, 65.0)
        self.assertEqual(goal.days_remaining, 14)
        self.assertFalse(goal.is_overdue)

        # Update via view
        resp = self.client.post(reverse('analytics:goal_update', kwargs={'pk': goal.pk}), {
            'title': goal.title,
            'metric_type': goal.metric_type,
            'target_value': '1000.00',
            'current_value': '1000.00',
            'start_date': today,
            'deadline': deadline,
            'status': 'active'
        })
        self.assertEqual(resp.status_code, 302)
        goal.refresh_from_db()
        self.assertEqual(goal.status, 'completed')
        self.assertEqual(goal.progress_percentage, 100.0)
