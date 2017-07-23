from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from . import models
from . import serializers


@api_view(['GET'])
def project_list(request):
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


@api_view(['GET', 'POST'])
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

    # Update project info for project with pk
    # Condition: Current User is the owner of this project
    # Accepts: Project Info Dictionary
    # Returns:
    #   SUCCESS: Project Page URL
    #   ERROR: Error Message
    if request.method == 'POST':
        if site_project.owner != request.user:
            return Response({
                'success': False,
                'error': 'User must be the owner to update the project'
            }, status=status.HTTP_401_UNAUTHORIZED)
        serializer = serializers.ProjectSerializer(instance=site_project,
                                                   data=request.data,
                                                   partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'project': serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'success': False,
                'project': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)


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
