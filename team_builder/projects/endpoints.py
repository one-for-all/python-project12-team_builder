from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.urls import reverse

from . import models
from . import serializers


@api_view(['GET', 'POST'])
def project_list(request):
    # Current: Lists all projects
    # List projects that meet supplied condition
    # Accepts: Condition Dictionary
    # Returns:
    #   SUCCESS: List of Project Info Dictionaries
    #   ERROR: Error message
    if request.method == 'GET':
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
            })

@api_view(['GET'])
def project(request, pk):
    try:
        site_project = models.SiteProject.objects.get(pk=pk)
    except models.SiteProject.DoesNotExist:
        return Response({
            'success': False,
            'error': 'Project does not exist'
        }, status=status.HTTP_400_BAD_REQUEST)

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


def application_list(request):
    # Get a list of applications by/for current user that meet supplied
    # conditions
    # Condition: User Logged In
    # Accepts: Condition Dictionary
    # Returns:
    #   SUCCESS: List of Application Info
    #   ERROR: Error Message
    if request.method == 'GET':
        pass


def application(request):
    # Get detailed info for an application with conditions by/for current user
    # Condition: User Logged In
    # Accepts: Condition Dictionary
    # Returns:
    #   SUCCESS: Application Info Dictionary
    #   ERROR: Error Message
    if request.method == 'GET':
        pass

    # Apply/Retract, Accept/Reject an application identified by condition
    # Condition: User Logged In
    # Accepts: Condition Dictionary
    # Returns:
    #   SUCCESS: Application redirect URL
    #   ERROR: Error Message
    if request.method == 'POST':
        pass
