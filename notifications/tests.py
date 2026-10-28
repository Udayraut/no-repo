from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Notification


class NotificationsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='notifuser', email='notif@skyniya.com', password='Password123!')
        self.client.force_login(self.user)
        self.notif = Notification.objects.create(
            user=self.user,
            title='Goal Milestone Reached',
            message='You reached 10,000 views on YouTube!',
            notification_type='goal_reached'
        )

    def test_notification_list_and_read(self):
        response = self.client.get(reverse('notifications:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Goal Milestone Reached')

        # Mark read
        read_resp = self.client.get(reverse('notifications:mark_read', kwargs={'pk': self.notif.pk}))
        self.assertEqual(read_resp.status_code, 302)
        self.notif.refresh_from_db()
        self.assertTrue(self.notif.is_read)
