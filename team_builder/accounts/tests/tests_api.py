from django.contrib.auth import get_user_model, get_user
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from accounts import models


# data is dictionary of lists and dictionaries
def sort_data(data):
    for key, val in data.items():
        if isinstance(val, dict):
            data[key] = sort_data(val)
        elif isinstance(val, list):
            data[key] = sorted(val)
    return data


def testSortedEqual(self, lfh, rhd):
    return self.assertEqual(sort_data(lfh), sort_data(rhd))


class SignUpTest(APITestCase):
    # post to api with modified data
    def post_create_user(self,  **kwargs):
        data = {
                'username': 'test',
                'email': 'test@example.com',
                'password': 'password',
                'confirm_password': 'password',
            }
        data.update(**kwargs)
        return self.client.post(
            reverse('accounts:api_signup'),
            data=data
        )


    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username='admin',
            email='admin@example.com',
            password='admin_you_cannot_guess_it'
        )

    def test_success_sign_up(self):
        resp = self.post_create_user()
        self.assertTrue(status.is_success(resp.status_code))
        user = get_user_model().objects.filter(username='test')
        self.assertTrue(user)

    def test_fail_sign_up_existing_username(self):
        resp = self.post_create_user(username='admin')
        self.assertTrue(status.is_client_error(resp.status_code))
        user = get_user_model().objects.filter(email='test@example.com')
        self.assertFalse(user)

    def test_fail_sign_up_invalid_username(self):
        resp = self.post_create_user(
            username='username cannot contain white spaces')
        self.assertTrue(status.is_client_error(resp.status_code))
        user = get_user_model().objects.filter(email='test@example.com')
        self.assertFalse(user)

    def test_fail_sign_up_existing_email(self):
        resp = self.post_create_user(email='admin@example.com')
        self.assertTrue(status.is_client_error(resp.status_code))
        user = get_user_model().objects.filter(username='test')
        self.assertFalse(user)

    def test_fail_sign_up_unmatched_password(self):
        resp = self.post_create_user(password='different_password')
        self.assertTrue(status.is_client_error(resp.status_code))
        user = get_user_model().objects.filter(username='test')
        self.assertFalse(user)


class LogInTest(APITestCase):
    # post to api with modified data
    def post_login_user(self, **kwargs):
        data = {
            'email': 'admin@example.com',
            'password': 'admin_you_cannot_guess_it',
        }
        data.update(**kwargs)
        return self.client.post(
            reverse('accounts:api_login'),
            data=data
        )

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username='admin',
            email='admin@example.com',
            password='admin_you_cannot_guess_it'
        )

    def test_success_login(self):
        resp = self.post_login_user()
        self.assertTrue(status.is_success(resp.status_code))
        user = get_user(self.client)
        self.assertTrue(user.is_authenticated)
        self.assertEqual(user, self.user)

    def test_fail_login_wrong_password(self):
        resp = self.post_login_user(password='wrong password')
        self.assertTrue(status.is_client_error(resp.status_code))
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)


class LogOutTest(APITestCase):
    def test_logout_success(self):
        self.user = get_user_model().objects.create_user(
            username='admin',
            email='admin@example.com',
            password='admin_you_cannot_guess_it'
        )
        self.client.force_login(self.user)
        resp = self.client.get(reverse('accounts:api_logout'))
        self.assertTrue(status.is_success(resp.status_code))
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)

    def test_logout_fail(self):
        resp = self.client.get(reverse('accounts:api_logout'))
        self.assertTrue(status.is_client_error(resp.status_code))


class ProfileTest(APITestCase):
    # Post to profile edit with updates
    def post_updated_profile(self, **kwargs):
        data = self.default_profile_data.copy()
        data.update(**kwargs)
        return self.client.post(reverse('accounts:api_profile'),
                                data=data)

    def create_profile(self):
        self.profile = models.UserProfile.objects.create(
            name=self.default_profile_data.get('name'),
            bio=self.default_profile_data.get('bio'),
            user=self.user
        )
        self.profile.skills.add(
            models.Skill.objects.create(name=self.default_profile_data.get(
                'skills')[0]),
            models.Skill.objects.create(name=self.default_profile_data.get(
                'skills')[1])
        )

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username='admin',
            email='admin@example.com',
            password='admin_you_cannot_guess_it'
        )
        cls.default_profile_data = {'name': 'Edward Admin',
                                    'bio': 'Wonderful Love',
                                    'avatar': None,
                                    'skills': ['Run', 'Jump']}

    def test_empty_profile_get(self):
        self.client.force_login(self.user)
        resp = self.client.get(reverse('accounts:api_profile'))
        self.assertEqual(
            resp.data, {'success': True,
                        'profile':
                            {'name': '',
                             'bio': '',
                             'avatar': None,
                             'skills': []
                             }
                        }
        )

    def test_nonempty_profile_get(self):
        self.create_profile()
        self.client.force_login(self.user)
        resp = self.client.get(reverse('accounts:api_profile'))
        self.assertTrue(status.is_success(resp.status_code))
        testSortedEqual(self, sort_data(resp.data), sort_data({
            'success': True,
            'profile': self.default_profile_data}
        ))

    def test_fail_get_not_logged_in(self):
        resp = self.client.get(reverse('accounts:api_profile'))
        self.assertTrue(status.is_client_error(resp.status_code))

    def test_fail_post_not_logged_in(self):
        resp = self.post_updated_profile()
        self.assertTrue(status.is_client_error(resp.status_code))

    def test_success_update_name(self):
        self.create_profile()
        self.client.force_login(self.user)
        resp = self.post_updated_profile(name='Alexander Admin')
        self.assertTrue(status.is_success(resp.status_code))
        updated_data = self.default_profile_data.copy()
        updated_data.update(name='Alexander Admin')
        testSortedEqual(self, sort_data(resp.data), sort_data({
            'success': True,
            'profile': updated_data}
        ))

    def test_success_update_skills(self):
        self.create_profile()
        self.client.force_login(self.user)
        resp = self.post_updated_profile(skills=['sing', 'dance'])
        self.assertTrue(status.is_success(resp.status_code))
        updated_data = self.default_profile_data.copy()
        updated_data.update(skills=['sing', 'dance'])
        testSortedEqual(self,
                        sort_data(resp.data),
                        sort_data({'success': True,
                                   'profile': updated_data}
                                  ))

class ProfileOtherTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username='admin',
            email='admin@example.com',
            password='admin_you_cannot_guess_it'
        )
        cls.default_profile_data = {'name': 'Edward Admin',
                                    'bio': 'Wonderful Love',
                                    'avatar': None,
                                    'skills': ['Run', 'Jump']}
        cls.profile = models.UserProfile.objects.create(
            name=cls.default_profile_data.get('name'),
            bio=cls.default_profile_data.get('bio'),
            user=cls.user
        )
        cls.profile.skills.add(
            models.Skill.objects.create(name=cls.default_profile_data.get(
                'skills')[0]),
            models.Skill.objects.create(name=cls.default_profile_data.get(
                'skills')[1])
        )

    def test_fail_no_username_matched(self):
        resp = self.client.get(reverse('accounts:api_profile_other', kwargs={
            'username': 'no_body_with_this_username'
        }))
        self.assertTrue(status.is_client_error(resp.status_code))

    def test_success(self):
        resp = self.client.get(reverse('accounts:api_profile_other', kwargs={
            'username': 'admin'
        }))
        self.assertTrue(status.is_success(resp.status_code))
        testSortedEqual(self, sort_data(resp.data), sort_data({
            'success': True,
            'profile': self.default_profile_data}
        ))
