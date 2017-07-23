from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from projects import models
from accounts import models as accounts_models


class ProjectListTest(APITestCase):
    fixtures = ['fixture_0001.json']

    @classmethod
    def setUpTestData(cls):
        cls.data = [
            {
                'title': 'Sing',
                'description': 'Sing for life',
                'timeline': '2 hours',
                'applicant_requirements': 'Good Voice',
                'positions': [
                    {
                        'title': 'Singer',
                        'description': 'Sing, Sing, Sing',
                        'skill': 'Sing'
                    },
                    {
                        'title': 'Listener',
                        'description': 'Listen with heart',
                        'skill': 'Listen'
                    },
                ]
            }
        ]
        cls.user = get_user_model().objects.create_user(
            username='admin',
            email='admin@example.com',
            password='admin_you_cannot_guess_it'
        )

    def test_success_empty(self):
        models.SiteProject.objects.all().delete()
        resp = self.client.get(reverse('projects:api_list'))
        self.assertTrue(status.is_success(resp.status_code))
        self.assertEqual(resp.data, {'success': True, 'projects': []})

    def test_success_fixture(self):
        projects = models.SiteProject.objects.all()
        resp = self.client.get(reverse('projects:api_list'))
        self.assertTrue(status.is_success(resp.status_code))
        resp_projects = resp.data.get('projects')
        self.assertEqual(len(projects), len(resp_projects))

    def test_success_post(self):
        self.client.force_login(self.user)
        existing_skill = accounts_models.Skill.objects.first()
        resp = self.client.post(reverse('projects:api_list'), data={
            'title': 'Publish an album',
            'description': 'Produce a great album',
            'timeline': '2 months',
            'applicant_requirements': '',
            'positions': [{
                'title': 'Singer',
                'description': 'Sing for the album',
                'skill': existing_skill.name
            }]
        })
        self.assertTrue(status.is_success(resp.status_code))
        projects = models.SiteProject.objects.filter(title='Publish an album',
                                                    owner=self.user)
        self.assertTrue(projects)
        position = models.Position.objects.filter(title='Singer',
                                                  project__in=projects)
        self.assertTrue(position)

    def test_fail_post_nouser(self):
        existing_skill = accounts_models.Skill.objects.first()
        resp = self.client.post(reverse('projects:api_list'), data={
            'title': 'Publish an album',
            'description': 'Produce a great album',
            'timeline': '2 months',
            'applicant_requirements': '',
            'positions': [{
                'title': 'Singer',
                'description': 'Sing for the album',
                'skill': existing_skill.name
            }]
        })
        self.assertTrue(status.is_client_error(resp.status_code))


class ProjectTest(APITestCase):
    fixtures = ['fixture_0001.json']

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username='admin',
            email='admin@example.com',
            password='admin_you_cannot_guess_it'
        )

    def test_success_get(self):
        site_project = models.SiteProject.objects.order_by('?').first()
        resp = self.client.get(reverse('projects:api_detail', kwargs={
            'pk': site_project.id
        }))
        self.assertTrue(status.is_success(resp.status_code))
        self.assertEqual(resp.data['project']['title'], site_project.title)
        titles = site_project.positions.all().values_list('title', flat=True)
        for position in resp.data['project']['positions']:
            self.assertIn(position['title'], titles)
