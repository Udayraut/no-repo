from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from .models import SocialPost, PostMetric, DailyLog


class TrackerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='growthtester', email='growth@skyniya.com', password='Password123!')
        self.other_user = User.objects.create_user(username='otheruser', email='other@skyniya.com', password='Password123!')
        
        self.post = SocialPost.objects.create(
            user=self.user,
            title='Growth Playbook 2026',
            platform='youtube',
            post_type='long_video',
            status='published',
            caption='Deep dive into modern content operations',
            tags='growth, strategy'
        )

    def test_post_creation_and_properties(self):
        self.assertEqual(str(self.post), '[YouTube] Growth Playbook 2026')
        self.assertEqual(self.post.total_views, 0)

        # Add manual metric
        metric = PostMetric.objects.create(
            post=self.post,
            metric_date=timezone.now().date(),
            source='MANUAL',
            views=1000,
            likes=120,
            comments=30,
            shares=15,
            saves=10
        )
        self.assertEqual(self.post.total_views, 1000)
        self.assertEqual(metric.total_engagement, 175)
        self.assertEqual(metric.engagement_rate, 17.5)

    def test_data_isolation(self):
        """User cannot see posts owned by other users."""
        self.client.force_login(self.other_user)
        response = self.client.get(reverse('tracker:post_list'))
        self.assertNotContains(response, 'Growth Playbook 2026')

        detail_response = self.client.get(reverse('tracker:post_detail', kwargs={'pk': self.post.pk}))
        self.assertEqual(detail_response.status_code, 404)

    def test_post_crud_authenticated(self):
        self.client.force_login(self.user)
        # Create
        create_resp = self.client.post(reverse('tracker:post_create'), {
            'title': 'New Instagram Reel',
            'platform': 'instagram',
            'post_type': 'reel_short',
            'status': 'draft',
            'caption': 'Exciting teaser coming soon #skyniya',
            'tags': 'teaser, reel'
        })
        self.assertEqual(create_resp.status_code, 302)
        new_post = SocialPost.objects.filter(title='New Instagram Reel').first()
        self.assertIsNotNone(new_post)
        self.assertEqual(new_post.user, self.user)

    def test_daily_log_flow(self):
        self.client.force_login(self.user)
        today = timezone.now().date()
        resp = self.client.post(reverse('tracker:daily_log'), {
            'log_date': today,
            'focus_area': 'SaaS Video Production',
            'content_items_created': 3,
            'hours_spent': 4.5,
            'productivity_score': 5,
            'key_learnings': 'B-roll pacing increased retention',
            'notes': 'Wrap up final thumbnail tomorrow'
        })
        self.assertEqual(resp.status_code, 302)
        log = DailyLog.objects.filter(user=self.user, log_date=today).first()
        self.assertIsNotNone(log)
        self.assertEqual(log.content_items_created, 3)
