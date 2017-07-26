from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import Http404
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout

from . import forms
from . import models

##########################################
# Refactor to use api
##########################################


def signup(request):
    return render(request, 'signup.html')


def signin(request):
    return render(request, 'signin.html')


def logout_user(request):
    if not request.user.is_authenticated():
        return Http404('Logged In User required')
    logout(request)
    return redirect(reverse('projects:home'))


def profile(request):
    if not request.user.is_authenticated():
        return Http404('Logged In User required')
    if not hasattr(request.user, 'profile'):
        models.UserProfile.objects.create(user=request.user)
    return render(request, 'profile.html')


def profile_edit(request):
    all_skills = models.Skill.objects.all()
    if not request.user.is_authenticated():
        return Http404('Logged In User required')
    if not hasattr(request.user, 'profile'):
        models.UserProfile.objects.create(user=request.user)
    return render(request, 'profile_edit.html', context={
        'all_skills': all_skills
    })


def profile_other(request, username):
    user = get_object_or_404(get_user_model(), username=username)
    return render(request, 'profile.html', context={
        'user': user
    })
