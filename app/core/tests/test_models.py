from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def sample_user(email="test@test.com", password='testpass'):
    """Create a sample test user"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):
    def test_creat_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = 'test@carteblanche.tech'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = 'test@CARTEBLANCHE.TECH'
        user = get_user_model().objects.create_user(email, 'test')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_creat_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'test@carteblanche.tech',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """Test tag string representation"""

        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Vegan'
        )

        self.assertEqual(str(tag), tag.name)
