from django.shortcuts import (render, Http404, redirect, reverse,
                              get_object_or_404)
from django.db.models import Q
from . import forms
from . import models
from accounts import models as account_models


def index(request):
    search_term = request.GET.get('term')
    skill = request.GET.get('skill')
    if search_term:
        projects = models.SiteProject.objects.filter(
            Q(title__icontains=search_term) |
            Q(description__icontains=search_term)
        )
    elif skill:
        projects = models.SiteProject.objects.filter(
            positions__skill=skill
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
    if request.user.is_authenticated:
        applied_positions = models.Position.objects.filter(
            project=project).filter(applications__applicant=request.user)
    else:
        applied_positions = models.Position.objects.none()
    pending_positions = applied_positions.filter(applications__status=0)
    approved_positions = applied_positions.filter(applications__status=1)
    rejected_positions = applied_positions.filter(applications__status=2)
    return render(request, 'project.html', context={
        'project': project,
        'pending_positions': pending_positions,
        'approved_positions': approved_positions,
        'rejected_positions': rejected_positions
    })


def view_applications(request):
    skills = account_models.Skill.objects.all()
    applications = models.Application.objects.filter(
        position__project__owner=request.user)
    return render(request, 'applications.html', context={
        'all_skills': skills,
        'applications': applications
    })
