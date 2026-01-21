from django.core.cache import cache
from django.urls import reverse
from rest_framework.test import APITestCase

from .models import User


class UserAPICacheTests(APITestCase):
    def setUp(self):
        cache.clear()
        self.user = User.objects.create_user(
            email="test@example.com",
            password="testpass123",
            user_type="passenger",
        )
        # Names come from DRF router in users/urls.py
        self.list_url = reverse("user-list")
        self.detail_url = reverse("user-detail", args=[self.user.id])

    def test_users_list_is_cached(self):
        # First request – should hit DB and set cache
        response1 = self.client.get(self.list_url)
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(len(response1.data), 1)

        # Add another user directly to DB (bypassing API)
        User.objects.create_user(
            email="another@example.com",
            password="testpass123",
            user_type="rider",
        )

        # Second request – should still return 1 user if cache is used
        response2 = self.client.get(self.list_url)
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(len(response2.data), 1)

    def test_users_list_cache_is_invalidated_on_create(self):
        response1 = self.client.get(self.list_url)
        self.assertEqual(len(response1.data), 1)

        # Create via API (should clear cache)
        create_response = self.client.post(
            self.list_url,
            {
                "email": "new@example.com",
                "password": "testpass123",
                "user_type": "passenger",
            },
            format="json",
        )
        self.assertEqual(create_response.status_code, 201)

        # Now list should see 2 users
        response2 = self.client.get(self.list_url)
        self.assertEqual(len(response2.data), 2)

    def test_user_detail_is_cached_and_invalidated_on_update(self):
        # First detail request – sets cache
        response1 = self.client.get(self.detail_url)
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response1.data["first_name"], "")

        # Update via API
        patch_response = self.client.patch(
            self.detail_url,
            {"first_name": "Updated"},
            format="json",
        )
        self.assertEqual(patch_response.status_code, 200)

        # Detail should reflect updated name (cache was invalidated)
        response2 = self.client.get(self.detail_url)
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(response2.data["first_name"], "Updated")
