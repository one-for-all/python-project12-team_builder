from django.db import models
from django.conf import settings
from accounts import models as accounts_models


POSITION_STATUSES = (
    (0, 'vacant'),
    (1, 'filled'),
    (2, 'approved'),
)


class Position(models.Model):
    title = models.CharField(max_length=140)
    description = models.TextField(blank=True, default='')
    status = models.SmallIntegerField(
        choices=POSITION_STATUSES,
        blank=True,
        default=0
    )
    applicant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='positions',
        null=True,
        blank=True
    )
    project = models.ForeignKey(
        'SiteProject',
        related_name='positions',
        on_delete=models.CASCADE
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
    applicant_requirements = models.TextField(blank=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='site_projects'
    )

    def __str__(self):
        return self.title
