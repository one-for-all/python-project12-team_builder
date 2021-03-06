from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import reverse, get_object_or_404
from django.contrib.auth import logout

from . import serializers
from accounts import models


@api_view(['POST'])
def signup(request):
    # Sign Up for an account
    # Accepts: Username, Email, Password, Confirm Password
    # Condition: Username matches [_\w]+
    # Returns:
    #   SUCCESS: Account Profile URL
    #   ERROR: { Field: Error }  Dictionary
    if request.method == 'POST':
        serializer = serializers.UserCreationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'account': serializer.data,
                'profile_url': reverse('accounts:profile')
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'success': False,
                'error': serializer.errors
            }, status=status.HTTP_409_CONFLICT)


@api_view(['POST'])
def login_user(request):
    # Log Into an account
    # Accepts: Email, Password
    # Returns:
    #   SUCCESS: Home Page URL
    #   ERROR: { Field: Error } Dictionary
    if request.method == 'POST':
        serializer = serializers.UserLogInSerializer(
            data=request.data,
            context={
                'request': request
            })
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'home_url': reverse('projects:home')
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'success': False,
                'error': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def logout_user(request):
    # Log Out an account
    # Condition: User Logged In
    # Return:
    #   SUCCESS: Redirect Page
    #   ERROR: Error Message
    if request.method == 'GET':
        logout(request)
        return Response({
            'success': True,
            'redirect_page': reverse('projects:home')
        }, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated, ))
def profile(request):
    # Get profile information for current user
    # Condition: User Logged In
    # Returns:
    #   SUCCESS: Profile Info Dictionary
    #   ERROR: Error Message
    if request.method == 'GET':
        user_profile, _ = models.UserProfile.objects.get_or_create(
            user=request.user)
        serializer = serializers.ProfileSerializer(user_profile)
        return Response({
            'success': True,
            'profile': serializer.data
        }, status=status.HTTP_200_OK)

    # Update profile for current user; Create profile if not exists
    # Condition: User Logged In
    # Accepts: Profile Info Dictionary
    # Returns:
    #   SUCCESS: Account Profile URL
    #   ERROR: { Field: Error } Dictionary
    if request.method == 'POST':
        user_profile, _ = models.UserProfile.objects.get_or_create(
            user=request.user)
        serializer = serializers.ProfileSerializer(instance=user_profile,
                                                   data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'profile': serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'success': False,
                'error': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def profile_avatar(request):
    avatar = request.FILES.get('avatar')
    request.user.profile.avatar = avatar
    request.user.profile.save()
    return Response({

    }, status=status.HTTP_200_OK)


@api_view(['GET'])
def profile_other(request, username):
    # Get profile info for user with username
    # Returns:
    #   SUCCESS: User Profile Info Dictionary
    #   ERROR: Error Message
    if request.method == 'GET':
        user_profile = get_object_or_404(models.UserProfile,
                                         user__username=username)
        serializer = serializers.ProfileSerializer(instance=user_profile)
        return Response({
            'success': True,
            'profile': serializer.data
        })
