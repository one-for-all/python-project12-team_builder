from django.shortcuts import (render, Http404, redirect, reverse,
                              get_object_or_404)
from django.db.models import Q
from . import forms
from . import models
from accounts import models as account_models


def index(request):
    search_term = request.GET.get('term')
    if search_term:
        projects = models.SiteProject.objects.filter(
            Q(title__icontains=search_term) |
            Q(description__icontains=search_term)
        )
    else:
        projects = models.SiteProject.objects.all()
    all_skills = account_models.Skill.objects.all()
    return render(request, 'index.html', context={
        'projects': projects,
        'all_skills': all_skills
    })


def new_project(request):
    if not request.user.is_authenticated():
        return Http404('Logged In user required')
    all_skills = account_models.Skill.objects.all()
    return render(request, 'project_new.html', context={
        'all_skills': all_skills
    })


def view_project(request, pk):
    project = get_object_or_404(models.SiteProject, pk=pk)
    return render(request, 'project.html', context={
        'project': project
    })


def view_applications(request):
    skills = account_models.Skill.objects.all()
    applications = models.Application.objects.filter(
        position__project__owner=request.user)
    return render(request, 'applications.html', context={
        'all_skills': skills,
        'applications': applications
    })
