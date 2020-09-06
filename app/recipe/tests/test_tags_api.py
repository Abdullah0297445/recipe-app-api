from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core import models
from recipe import serializers


TAG_URL = reverse('recipe:tag-list')


class PublicTagsApiTest(TestCase):
    """Test the pubicly available tags API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to retrieve tags"""
        res = self.client.get(TAG_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTests(TestCase):
    """Test the authorized user tag API"""
    def setUp(self):
        self.user = get_user_model().objects.create(
            email="test@test.com",
            password="testpass"
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        """Test retrieving tags"""
        models.Tag.objects.create(user=self.user, name='Vegan')
        models.Tag.objects.create(user=self.user, name='Dessert')

        res = self.client.get(TAG_URL)

        tags = models.Tag.objects.all().order_by("-name")
        serializer = serializers.TagSerializer(tags, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):
        """Test tags list is only shown to the authenticated user"""
        user2 = get_user_model().objects.create_user(
            email="other@test.com",
            password="testpass"
        )
        models.Tag.objects.create(user=user2, name="Fruity")
        tag = models.Tag.objects.create(user=self.user, name="Fish")

        res = self.client.get(TAG_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)
