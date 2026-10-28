from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse


class DashboardTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='dashuser', email='dash@skyniya.com', password='Password123!')

    def test_dashboard_redirect_anonymous(self):
        response = self.client.get(reverse('dashboard:index'))
        self.assertEqual(response.status_code, 302)

    def test_dashboard_authenticated_load(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('dashboard:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Growth Overview')
