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

    def test_create_tag_successful(self):
        """Test creating a new tag"""
        payload = {'name': 'Test tag'}

        self.client.post(TAG_URL, payload)
        exists = models.Tag.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()

        self.assertTrue(exists)

    def test_valid_name_tag(self):
        """Test creating a new tag with invalid payload"""
        payload = {'name': ''}
        res = self.client.post(TAG_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_tags_assigned_to_recipes(self):
        """Test retrieving tags asasigned to particular recipe"""
        tag1 = models.Tag.objects.create(user=self.user, name='Tag 1')
        tag2 = models.Tag.objects.create(user=self.user, name='Tag 2')

        recipe = models.Recipe.objects.create(
            title='sample recipe',
            price=3,
            time=4,
            user=self.user
        )
        recipe.tags.add(tag1)

        res = self.client.get(TAG_URL, {'assigned_only': 1})

        serializer1 = serializers.TagSerializer(tag1)
        serializer2 = serializers.TagSerializer(tag2)
        self.assertIn(serializer1.data, res.data)
        self.assertNotIn(serializer2.data, res.data)

    def test_retrieve_unique_tags(self):
        """Test that retrieved tags are unique"""
        tag = models.Tag.objects.create(user=self.user, name='Drink')
        models.Tag.objects.create(user=self.user, name='tag')

        recipe1 = models.Recipe.objects.create(
            title='sample recipe',
            price=2,
            time=5,
            user=self.user
        )
        recipe2 = models.Recipe.objects.create(
            title='sample recipe 2',
            price=2,
            time=5,
            user=self.user
        )
        recipe1.tags.add(tag)
        recipe2.tags.add(tag)

        res = self.client.get(TAG_URL, {'assigned_only': 1})
        self.assertEqual(len(res.data), 1)
