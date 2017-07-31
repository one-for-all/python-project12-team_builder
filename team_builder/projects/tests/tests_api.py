from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from projects import models
from accounts import models as accounts_models


class ProjectListTest(APITestCase):
    fixtures = ['fixture_0002.json']

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

    def test_success_filter_by_term(self):
        project = models.SiteProject.objects.order_by('?').first()
        term = project.title.lower()
        resp = self.client.get(reverse('projects:api_list'), data={
            'term': term.upper()
        })
        resp_projects = resp.data.get('projects')
        for project in resp_projects:
            self.assertTrue(
                (term in project.get('title').lower()) or
                (term in project.get('description').lower())
            )


class ProjectTest(APITestCase):
    fixtures = ['fixture_0002.json']

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


class ApplicationListTest(APITestCase):
    fixtures = ['fixture_0002.json']

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username='admin',
            email='admin@example.com',
            password='admin_you_cannot_guess_it'
        )

    def test_success_post(self):
        self.client.force_login(self.user)
        position = models.Position.objects.order_by('?').first()
        resp = self.client.post(reverse('projects:api_application_list'),
                                data={'position_id': position.id})
        self.assertTrue(status.is_success(resp.status_code))
        application_id = resp.data['application']['id']
        application = models.Application.objects.get(pk=application_id)
        self.assertEqual(application.applicant, self.user)

    def test_success_list_by(self):
        user = get_user_model().objects.order_by('?').first()
        self.client.force_login(user)
        resp = self.client.get(reverse('projects:api_application_list'),
                               data={'relation': 'by'})
        self.assertTrue(status.is_success(resp.status_code))
        for application_data in resp.data['applications']:
            self.assertEqual(application_data['applicant'], user.id)

    def test_success_list_for(self):
        user = get_user_model().objects.order_by('?').first()
        self.client.force_login(user)
        resp = self.client.get(reverse('projects:api_application_list'),
                               data={'relation': 'for'})
        self.assertTrue(status.is_success(resp.status_code))
        for application_data in resp.data['applications']:
            position_id = application_data['position']
            position = models.Position.objects.get(pk=position_id)
            self.assertEqual(position.project.owner, user)

    def test_fail_list_no_user(self):
        resp = self.client.get(reverse('projects:api_application_list'),
                               data={'relation': 'for'})
        self.assertTrue(status.is_client_error(resp.status_code))
        resp = self.client.get(reverse('projects:api_application_list'),
                               data={'relation': 'by'})
        self.assertTrue(status.is_client_error(resp.status_code))


class ApplicationDetailTest(APITestCase):
    fixtures = ['fixture_0002.json']

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username='admin',
            email='admin@example.com',
            password='admin_you_cannot_guess_it'
        )

    def test_fail_get_invalid_id(self):
        count = models.Application.objects.count()
        resp = self.client.get(reverse('projects:api_application', kwargs={
            'pk': count+1
        }))
        self.assertTrue(status.is_client_error(resp.status_code))

    def test_success_get(self):
        application = models.Application.objects.order_by('?').first()
        resp = self.client.get(reverse('projects:api_application', kwargs={
            'pk': application.id
        }))
        self.assertTrue(status.is_success(resp.status_code))
        self.assertEqual(resp.data['application']['status'],
                         application.status)
        self.assertEqual(resp.data['application']['applicant'], application.applicant.id)

    def test_success_retract(self):
        application = models.Application.objects.order_by('?').first()
        user = application.applicant
        self.client.force_login(user)
        resp = self.client.post(reverse('projects:api_application', kwargs={
            'pk': application.id
        }), data={'action': 'retract'})
        self.assertTrue(status.is_success(resp.status_code))
        application = models.Application.objects.filter(pk=application.id)
        self.assertFalse(application)

    def test_fail_retract_not_applicant(self):
        application = models.Application.objects.order_by('?').first()
        self.client.force_login(self.user)
        resp = self.client.post(reverse('projects:api_application', kwargs={
            'pk': application.id
        }), data={'action': 'retract'})
        self.assertTrue(status.is_client_error(resp.status_code))

    def test_success_accept(self):
        application = models.Application.objects.order_by('?').first()
        user = application.position.project.owner
        self.client.force_login(user)
        resp = self.client.post(reverse('projects:api_application', kwargs={
            'pk': application.id
        }), data={'action': 'approve'})
        self.assertTrue(status.is_success(resp.status_code))
        application.refresh_from_db()
        self.assertEqual(application.status, 1)

    def test_fail_accept_not_owner(self):
        application = models.Application.objects.order_by('?').first()
        self.client.force_login(self.user)
        resp = self.client.post(reverse('projects:api_application', kwargs={
            'pk': application.id
        }), data={'action': 'accept'})
        self.assertTrue(status.is_client_error(resp.status_code))

    def test_success_reject(self):
        application = models.Application.objects.order_by('?').first()
        user = application.position.project.owner
        self.client.force_login(user)
        resp = self.client.post(reverse('projects:api_application', kwargs={
            'pk': application.id
        }), data={'action': 'reject'})
        self.assertTrue(status.is_success(resp.status_code))
        application.refresh_from_db()
        self.assertEqual(application.status, 2)

    def test_fail_reject_not_owner(self):
        application = models.Application.objects.order_by('?').first()
        self.client.force_login(self.user)
        resp = self.client.post(reverse('projects:api_application', kwargs={
            'pk': application.id
        }), data={'action': 'reject'})
        self.assertTrue(status.is_client_error(resp.status_code))