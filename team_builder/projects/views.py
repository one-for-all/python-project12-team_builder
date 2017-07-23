import json
from django.shortcuts import (render, Http404, redirect, reverse,
                              get_object_or_404)
from django.views.decorators.csrf import csrf_exempt

from . import forms
from . import models
from accounts import models as account_models


def index(request):
    return render(request, 'index.html')


def new_project(request):
    if not request.user.is_authenticated():
        return Http404('Logged In user required')
    all_skills = account_models.Skill.objects.all()
    if request.method == 'POST':
        form = forms.NewProjectForm(
            project=None,
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
            return render(request, 'project_edit.html', context={
                'all_skills': all_skills,
                'form_errors': form_errors
            })
    return render(request, 'project_edit.html', context={
        'all_skills': all_skills
    })


def view_project(request, pk):
    project = get_object_or_404(models.SiteProject, pk=pk)
    return render(request, 'project.html', context={
        'project': project
    })


@csrf_exempt
def edit_project(request, pk):
    if request.method == 'POST':
        print(request.body.decode("utf-8"))
        print(json.loads(request.body.decode("utf-8")))
    project = get_object_or_404(models.SiteProject, pk=pk)
    # if request.user != project.owner:
    #     return Http404('Owner required')
    all_skills = account_models.Skill.objects.all()
    return render(request, 'project_edit.html', context={
        'all_skills': all_skills,
        'project': project
    })
