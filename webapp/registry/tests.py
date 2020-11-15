from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Appointment
from datetime import datetime

# Create your tests here.
class AppointmentTestCase(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        User.objects.create_user(**self.credentials)

    def test_home_url_without_auth(self):
        response = self.client.get(reverse('home', args=[]))
        self.assertEqual(response.status_code, 302)

    def test_login_url_get_without_auth(self):
        response = self.client.get(reverse('login', args=[]))
        self.assertEqual(response.status_code, 200)

    def test_login_url_post(self):
        response = self.client.post(reverse('login'), self.credentials, follow=True)
        self.assertTrue(response.context['user'].is_active)

    def test_home_url_with_auth(self):
        response = self.client.post(reverse('login'), self.credentials, follow=True)
        response = self.client.get(reverse('home', args=[]))
        self.assertEqual(response.status_code, 200)

    def test_login_url_get_with_auth(self):
        response = self.client.post(reverse('login'), self.credentials, follow=True)
        response = self.client.get(reverse('login', args=[]))
        self.assertEqual(response.status_code, 302)

    def test_appointments_new_url(self):
        # no login
        response = self.client.get(reverse('appointment_new', args=[]))
        self.assertEqual(response.status_code, 302)
        # logged in
        response = self.client.post(reverse('login'), self.credentials, follow=True)
        response = self.client.get(reverse('appointment_new', args=[]))
        self.assertEqual(response.status_code, 200)
        # add appointment
        myuser = User.objects.get(pk=1)
        today = datetime.today().strftime('%Y-%m-%dT%H:%M')
        data = {"datetime": today,
                "province": "SJ",
                "provider": "O1",
                "latitude": 0.0,
                "longitude": 0.0,
                "alias": "Appointment Test",
                "owner": myuser}
        response = self.client.post(reverse('appointment_new'), data, follow=True)
        self.assertEqual(response.status_code, 200)
