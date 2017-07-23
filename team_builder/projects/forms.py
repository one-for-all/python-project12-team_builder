from django.forms import forms, fields

from . import models
from accounts import models as accounts_models


class NewProjectForm(forms.Form):
    def __init__(self, project, owner, positions, *args, **kwargs):
        self.project = project
        self.owner = owner
        self.positions = positions
        super().__init__(*args, **kwargs)

    title = fields.CharField(max_length=140)
    description = fields.CharField()
    timeline = fields.CharField(max_length=255)
    applicant_requirements = fields.CharField()

    def save(self):
        if self.project is None:
            project = models.SiteProject.objects.create(owner=self.owner)
        else:
            project = self.project
        project.title = self.cleaned_data['title']
        project.description = self.cleaned_data['description']
        project.timeline = self.cleaned_data['timeline']
        project.applicant_requirements = self.cleaned_data[
            "applicant_requirements"]
        project.positions.all().delete()
        for title, description, skill in self.positions:
            try:
                skill_object = accounts_models.Skill.objects.get(name=skill)
            except accounts_models.Skill.DoesNotExist:
                skill_object = None
            models.Position.objects.create(
                title=title,
                description=description,
                status=0,
                project=project,
                skill=skill_object
            )
        project.save()
