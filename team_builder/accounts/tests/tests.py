from django.test import TestCase
from django.contrib.auth import get_user_model, get_user
from django.shortcuts import reverse

from accounts import forms
from accounts import models


def create_test_user():
    return get_user_model().objects.create_user(
        username='test',
        email='test@example.com',
        password='password'
    )


class SignInViewTest(TestCase):
    def test_invalid_signin(self):
        resp = self.client.post(
            reverse('accounts:signin'),
            data={
                'email': 'test@example.com',
                'password': 'password'
            }
        )
        self.assertContains(resp, 'Error')
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)

    def test_valid_signin(self):
        create_test_user()
        self.client.post(
            reverse('accounts:signin'),
            data={
                'email': 'test@example.com',
                'password': 'password'
            }
        )
        user = get_user(self.client)
        self.assertTrue(user.is_authenticated)


class LogOutViewTest(TestCase):
    def test_success_logout(self):
        create_test_user()
        self.client.post(
            reverse('accounts:signin'),
            data={
                'email': 'test@example.com',
                'password': 'password'
            }
        )
        self.client.get(reverse('accounts:logout'))
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)


class ProfileViewTest(TestCase):
    def test_empty_profile_creation(self):
        user = create_test_user()
        self.client.force_login(user)
        self.assertFalse(hasattr(user, 'profile'))
        self.client.get(reverse('accounts:profile'))
        user = get_user_model().objects.get(username='test')
        self.assertTrue(hasattr(user, 'profile'))

    def test_existing_profile_noncreation(self):
        user = create_test_user()
        profile = models.UserProfile.objects.create(user=user)
        profile.name = 'Jay'
        self.client.force_login(user)
        self.client.get(reverse('accounts:profile'))
        user = get_user_model().objects.get(username='test')
        self.assertEqual(user.profile, profile)
