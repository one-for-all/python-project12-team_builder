from django.forms import forms, fields
from django.contrib.auth import get_user_model

from . import models


class SignUpForm(forms.Form):
    username = fields.CharField()
    email = fields.EmailField()
    password1 = fields.CharField()
    password2 = fields.CharField()

    def clean_email(self):
        try:
            email = self.cleaned_data['email']
        except KeyError:
            raise forms.ValidationError(
                'Email is required'
            )
        user_model = get_user_model()
        try:
            user_model.objects.get(email=email)
        except user_model.DoesNotExist:
            return email
        else:
            raise forms.ValidationError(
                'This email has been used'
            )

    def clean_username(self):
        try:
            username = self.cleaned_data['username']
        except KeyError:
            raise forms.ValidationError(
                'Username is required'
            )
        user_model = get_user_model()
        try:
            user_model.objects.get(username=username)
        except user_model.DoesNotExist:
            return username
        else:
            raise forms.ValidationError(
                'This username has been used'
            )

    def clean(self):
        cleaned_data = super().clean()
        try:
            password1 = cleaned_data['password1']
            password2 = cleaned_data['password2']
        except KeyError:
            raise forms.ValidationError(
                'passwords are required'
            )
        if cleaned_data['password1'] != cleaned_data['password2']:
            raise forms.ValidationError(
                'Passwords need to match'
            )

    def save(self):
        get_user_model().objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password1']
        )


class ProfileForm(forms.Form):
    def __init__(self, user_profile, *args, **kwargs):
        self.user_profile = user_profile
        super().__init__(*args, **kwargs)

    name = fields.CharField(max_length=140)
    bio = fields.CharField()

    def save(self):
        self.user_profile.name = self.cleaned_data.get('name')
        self.user_profile.bio = self.cleaned_data.get('bio')
        self.user_profile.save()


class SkillsForm:
    def __init__(self, user_profile, skills):
        self.user_profile = user_profile
        self.skills = skills

    def is_valid(self):
        return True

    def _clean(self):
        self.skills = [skill.strip() for skill in self.skills]

    def save(self):
        self._clean()
        skill_objects = []
        for skill in self.skills:
            if not skill == '':
                skill_object, _ = models.Skill.objects.get_or_create(
                    name=skill)
                skill_objects.append(skill_object)
        self.user_profile.skills.set(skill_objects)
        self.user_profile.save()
