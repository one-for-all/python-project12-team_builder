from django.shortcuts import render, Http404, redirect, reverse

from . import forms
from accounts import models as account_models


def index(request):
    return render(request, 'index.html')


def new_project(request):
    if not request.user.is_authenticated():
        return Http404('Logged In user required')
    all_skills = account_models.Skill.objects.all()
    if request.method == 'POST':
        form = forms.NewProjectForm(
            owner=request.user,
            positions=zip(request.POST.getlist('position_title'),
                          request.POST.getlist('position_description'),
                          request.POST.getlist('skills')),
            data=request.POST
        )
        if form.is_valid():
            form.save()
            return redirect(reverse('projects:home'))
        else:
            form_errors = form.errors
            return render(request, 'project_new.html', context={
                'all_skills': all_skills,
                'form_errors': form_errors
            })
    return render(request, 'project_new.html', context={
        'all_skills': all_skills
    })
