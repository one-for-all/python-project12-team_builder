from django.shortcuts import render, redirect, reverse
from django.http import Http404
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout

from . import forms
from . import models


def signup(request):
    if request.method == 'POST':
        form = forms.SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('projects:home'))
        else:
            return render(request, 'signup.html', context={
                'form_errors': form.errors
            })
    return render(request, 'signup.html')


def signin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            return redirect(reverse('projects:home'))
        else:
            return render(request, 'signin.html', context={
                'error': 'Invalid Login'
            })
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
    if request.method == 'POST':
        print(request.POST)
        form = forms.ProfileForm(
            user_profile=request.user.profile,
            data=request.POST
        )
        skills_form = forms.SkillsForm(
            user_profile=request.user.profile,
            skills=request.POST.getlist('skills')
        )
        if form.is_valid() and skills_form.is_valid():
            form.save()
            skills_form.save()
            return redirect(reverse('accounts:profile'))
        else:
            form_errors = form.errors
            return render(request, 'profile_edit.html', context={
                'all_skills': all_skills,
                'form_errors': form_errors
            })
    return render(request, 'profile_edit.html', context={
        'all_skills': all_skills
    })
