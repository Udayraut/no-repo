from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import UserProfile


class AccountsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testgrowthuser',
            email='user@skyniya.com',
            password='SecretPassword123!'
        )

    def test_profile_signal_creation(self):
        """Check that UserProfile is automatically generated on User creation."""
        self.assertTrue(hasattr(self.user, 'profile'))
        self.assertIsInstance(self.user.profile, UserProfile)
        self.assertEqual(self.user.profile.timezone, 'UTC')

    def test_profile_view_login_required(self):
        """Unauthenticated requests must redirect to login."""
        response = self.client.get(reverse('accounts:profile'))
        self.assertEqual(response.status_code, 302)

    def test_settings_authenticated_access(self):
        """Authenticated users can access settings page."""
        self.client.force_login(self.user)
        response = self.client.get(reverse('accounts:settings'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Account Settings')
