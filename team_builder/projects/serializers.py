from rest_framework import serializers

from . import models


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Position
        fields = ['title', 'description', 'skill']


class ProjectSerializer(serializers.ModelSerializer):
    positions = PositionSerializer(many=True)

    class Meta:
        model = models.SiteProject
        fields = ['title', 'description', 'timeline',
                  'applicant_requirements', 'owner', 'positions']
        extra_kwargs = {
            'owner': {'read_only': True}
        }
