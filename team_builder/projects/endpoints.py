from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import (IsAuthenticatedOrReadOnly,
                                        IsAuthenticated)
from rest_framework.response import Response
from rest_framework import status
from django.urls import reverse
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail

from . import models
from . import serializers


@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticatedOrReadOnly, ))
def project_list(request):
    # Current: Lists all projects
    # List projects that meet supplied condition
    # Accepts: Condition Dictionary
    # Returns:
    #   SUCCESS: List of Project Info Dictionaries
    #   ERROR: Error message
    if request.method == 'GET':
        search_term = request.GET.get('term')
        if search_term:
            projects = models.SiteProject.objects.filter(
                Q(title__icontains=search_term) |
                Q(description__icontains=search_term)
            )
        else:
            projects = models.SiteProject.objects.all()
        serializer = serializers.ProjectSerializer(instance=projects,
                                                   many=True)
        return Response({
            'success': True,
            'projects': serializer.data
        }, status=status.HTTP_200_OK)

    # Post a new project by current user
    # Condition: User Logged In
    # Accepts: Project Info Dictionary
    # Returns:
    #   SUCCESS: Project Info, Project Detail URL
    #   ERROR: Error message
    if request.method == 'POST':
        serializer = serializers.ProjectSerializer(data=request.data,
                                                   context={
                                                       'owner': request.user
                                                   })
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'project': serializer.data,
                'project_url': reverse('projects:view', kwargs={
                    'pk': serializer.data.get('id')})
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'success': False,
                'error': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def project(request, pk):
    site_project = get_object_or_404(models.SiteProject, pk=pk)

    # Get project info for project with pk
    # Returns:
    #   SUCCESS: Project Info Dictionary
    #   ERROR: Error Message
    if request.method == 'GET':
        serializer = serializers.ProjectSerializer(instance=site_project)
        return Response({
            'success': True,
            'project': serializer.data
        }, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated, ))
def application_list(request):
    # Get a list of applications by/for current user that meet supplied
    # conditions
    # Condition: User Logged In
    # Accepts: Condition Dictionary
    # Returns:
    #   SUCCESS: List of Application Info
    #   ERROR: Error Message
    if request.method == 'GET':
        relation = request.query_params.get('relation')
        if relation == 'by':
            applications = models.Application.objects.filter(
                applicant=request.user)
        elif relation == 'for':
            applications = models.Application.objects.filter(
                position__project__owner=request.user
            )
        else:
            return Response({
            'error': 'Invalid relation'
        }, status=status.HTTP_400_BAD_REQUEST)
        serializer = serializers.ApplicationSerializer(
            instance=applications, many=True)
        return Response({
            'applications': serializer.data
        }, status=status.HTTP_200_OK)

    # Apply for an position by current user
    # Condition: User Logged In
    # Accepts: position id
    # Returns:
    #   SUCCESS: Application Info Dict
    #   ERROR: Error Message
    if request.method == 'POST':
        position_id = request.data.get('position_id')
        position = get_object_or_404(models.Position, pk=position_id)
        if position.project.owner == request.user:
            return Response({
                'error': 'Cannot apply for own project'
            }, status=status.HTTP_400_BAD_REQUEST)
        application = position.applications.create(applicant=request.user)
        serializer = serializers.ApplicationSerializer(instance=application)
        return Response({
            'application': serializer.data
        }, status=status.HTTP_201_CREATED)


@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticatedOrReadOnly, ))
def application_detail(request, pk):
    application = get_object_or_404(models.Application, pk=pk)

    # Get detailed info of an application
    # Returns:
    #   SUCCESS: Application Info Dictionary
    #   ERROR: Error Message
    if request.method == 'GET':
        serializer = serializers.ApplicationSerializer(instance=application)
        return Response({
            'application': serializer.data
        }, status=status.HTTP_200_OK)

    # Retract, Accept/Reject an application identified by condition
    # Condition: User Logged In
    # Accepts: Condition Dictionary
    # Returns:
    #   SUCCESS: Application redirect URL
    #   ERROR: Error Message
    if request.method == 'POST':
        action = request.data.get('action')
        if action == 'retract':
            if application.applicant != request.user:
                return Response({
                    'error': 'Current User needs to be the applicant to '
                             'retract'
                }, status=status.HTTP_401_UNAUTHORIZED)
            else:
                application.delete()
                return Response({
                    'message': 'Application retracted'
                }, status=status.HTTP_202_ACCEPTED)
        elif action == 'approve':
            if application.position.project.owner != request.user:
                return Response({
                    'error': 'Current User needs to be the owner to accept'
                }, status=status.HTTP_401_UNAUTHORIZED)
            else:
                application.status = 1
                application.save()
                send_mail(
                    'You application approved',
                    'Your application to {} for {} has been approved.'.format(
                        application.position.title,
                        application.position.project.title),
                    'team_builder@example.com',
                    [application.applicant.email]
                )
                return Response({
                    'message': 'Application accepted'
                }, status=status.HTTP_202_ACCEPTED)
        elif action == 'reject':
            if application.position.project.owner != request.user:
                return Response({
                    'error': 'Current User needs to be the owner to reject'
                }, status=status.HTTP_401_UNAUTHORIZED)
            else:
                application.status = 2
                application.save()
                send_mail(
                    'You application rejected',
                    'Your application to {} for {} has been rejected.'.format(
                        application.position.title,
                        application.position.project.title),
                    'team_builder@example.com',
                    [application.applicant.email]
                )
                return Response({
                    'message': 'Application rejected'
                }, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({
                'error': {
                    'non_field_errors': 'Invalid action'
                }
            }, status=status.HTTP_400_BAD_REQUEST)
