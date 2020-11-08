from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Asset

# Create your tests here.
class AssetTestCase(TestCase):
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

    def test_assets_new_url(self):
        # no login
        response = self.client.get(reverse('asset_new', args=[]))
        self.assertEqual(response.status_code, 302)
        # logged in
        response = self.client.post(reverse('login'), self.credentials, follow=True)
        response = self.client.get(reverse('asset_new', args=[]))
        self.assertEqual(response.status_code, 200)
        # add asset
        myuser = User.objects.get(pk=1)
        data = {"alias": "alias1", "province": "province1", "category": "I", "latitude": 0.0, "longitude": 0.0, "owner": myuser}
        response = self.client.post(reverse('asset_new'), data, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_assets_read_url(self):
        response = self.client.post(reverse('login'), self.credentials, follow=True)
        myuser = User.objects.get(pk=1)
        data = {"alias": "alias1", "province": "province1", "category": "I", "latitude": 0.0, "longitude": 0.0, "owner": myuser}
        response = self.client.post(reverse('asset_new'), data, follow=True)
        # valid pk
        response = self.client.get(reverse('asset_read', args=(1,)), data, follow=True)
        self.assertEqual(response.status_code, 200)
        # invalid pk
        response = self.client.get(reverse('asset_read', args=(2,)), data, follow=True)
        self.assertEqual(response.status_code, 404)