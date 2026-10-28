from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from tracker.models import SocialPost


class ReportsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='reportuser', email='reports@skyniya.com', password='Password123!')
        self.client.force_login(self.user)
        SocialPost.objects.create(
            user=self.user,
            title='Sample Export Post',
            platform='twitter',
            status='published',
            caption='Growth hacking insights'
        )

    def test_reports_index_view(self):
        response = self.client.get(reverse('reports:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Export Center')

    def test_csv_export_posts(self):
        response = self.client.get(reverse('reports:export_posts_csv'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')
        self.assertIn('Sample Export Post', response.content.decode('utf-8'))
