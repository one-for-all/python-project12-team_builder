from django.test import TestCase
from django.contrib.auth import get_user_model, get_user
from django.shortcuts import reverse

from . import forms
from . import models


def create_test_user():
    return get_user_model().objects.create_user(
        username='test',
        email='test@example.com',
        password='password'
    )


class SignupFormTest(TestCase):
    def test_form_empty_fields(self):
        form = forms.SignUpForm({})
        self.assertFalse(form.is_valid())
        form = forms.SignUpForm({
            'username': 'test',
            'email': 'test@example.com',
            'password1': 'password',
        })
        self.assertFalse(form.is_valid())
        form = forms.SignUpForm({
            'username': 'test',
            'email': 'test@example.com',
            'password2': 'password',
        })
        self.assertFalse(form.is_valid())
        form = forms.SignUpForm({
            'username': 'test',
            'password1': 'password',
            'password2': 'password',
        })
        self.assertFalse(form.is_valid())
        form = forms.SignUpForm({
            'email': 'test@example.com',
            'password1': 'password',
            'password2': 'password',
        })
        self.assertFalse(form.is_valid())
        form = forms.SignUpForm({
            'username': 'test',
            'email': 'test@example.com',
            'password1': 'password',
            'password2': 'password',
        })
        self.assertTrue(form.is_valid())

    def test_unmatched_password(self):
        form = forms.SignUpForm({
            'username': 'test',
            'email': 'test@example.com',
            'password1': 'password',
            'password2': 'different_password',
        })
        self.assertFalse(form.is_valid())

    def test_repeated_username(self):
        user_model = get_user_model()
        user_model.objects.create_user(
            username='test',
            email='test@example.com',
            password='password'
        )
        form = forms.SignUpForm({
            'username': 'test',
            'email': 'test2@example.com',
            'password1': 'password',
            'password2': 'password',
        })
        self.assertFalse(form.is_valid())

    def test_repeated_email(self):
        user_model = get_user_model()
        user_model.objects.create_user(
            username='test',
            email='test@example.com',
            password='password'
        )
        form = forms.SignUpForm({
            'username': 'test2',
            'email': 'test@example.com',
            'password1': 'password',
            'password2': 'password',
        })
        self.assertFalse(form.is_valid())


class SignupViewTest(TestCase):
    def test_invalid_form(self):
        resp = self.client.post(
            reverse('accounts:signup'),
            data={
                'username': 'test',
                'email': 'test@example.com',
                'password1': 'password',
                'password2': 'different password',
            }
        )
        self.assertContains(resp, 'Error')

    def test_valid_form(self):
        self.client.post(
            reverse('accounts:signup'),
            data={
                'username': 'test',
                'email': 'test@example.com',
                'password1': 'password',
                'password2': 'password',
            }
        )
        user = get_user_model().objects.get(username='test')
        self.assertIsNotNone(user)
        self.assertEqual(user.email, 'test@example.com')


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


class ProfileEditViewTest(TestCase):
    def test_success_change(self):
        user = create_test_user()
        self.client.force_login(user)
        self.client.post(reverse('accounts:profile_edit'), data={
            'name': 'Jay',
            'bio': 'Wonderful Love',
            'skills': ['python', 'django'],
        })
        user_profile = models.UserProfile.objects.get(user=user)
        self.assertEqual(user_profile.name, 'Jay')
        self.assertEqual(user_profile.bio, 'Wonderful Love')
        skills = models.Skill.objects.filter(
            name__in=['python', 'django']
        )
        self.assertQuerysetEqual(user_profile.skills.all(), map(repr, skills),
                                 ordered=False)
