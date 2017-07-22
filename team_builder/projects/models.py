from django.db import models
from django.conf import settings
from accounts import models as accounts_models


POSITION_STATUSES = (
    (0, 'vacant'),
    (1, 'applied'),
    (2, 'filled')
)


class Position(models.Model):
    title = models.CharField(max_length=140)
    description = models.TextField()
    status = models.SmallIntegerField(
        choices=POSITION_STATUSES
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='positions',
        null=True,
        blank=True
    )
    project = models.ForeignKey(
        'SiteProject',
        related_name='positions',
    )
    skill = models.ForeignKey(
        accounts_models.Skill,
        related_name='positions',
        null=True,
        blank=True
    )

    def __str__(self):
        return "{} for {}".format(self.title, str(self.project))


class SiteProject(models.Model):
    title = models.CharField(max_length=140)
    description = models.TextField()
    timeline = models.CharField(max_length=255)
    applicant_requirements = models.TextField()
    url = models.URLField(null=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='site_projects'
    )

    def __str__(self):
        return self.title
