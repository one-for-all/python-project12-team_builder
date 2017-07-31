from django.test import TestCase
from django.contrib.auth import get_user_model
from django.shortcuts import reverse

from projects import models


def create_user():
    return get_user_model().objects.create_user(
        username='new_user',
        email='new_user@example.com',
        password='password'
    )


def create_project(owner):
    return models.SiteProject.objects.create(
        title='Sing',
        description='Sing for life',
        timeline='1 hour',
        applicant_requirements='Good Voice',
        owner=owner
    )


class ViewProjectViewTest(TestCase):
    def test_success_view(self):
        user = create_user()
        project = create_project(user)
        resp = self.client.get(reverse('projects:view', kwargs={
            'pk': project.id
        }))
        self.assertContains(resp, project.title)
