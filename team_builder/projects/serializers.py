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
        fields = ['id', 'title', 'description', 'timeline',
                  'applicant_requirements', 'owner', 'positions']
        extra_kwargs = {
            'owner': {'read_only': True},
            'id': {'read_only': True},
        }

    def create(self, validated_data):
        owner = self.context.get('owner')
        if not owner.is_authenticated:
            raise serializers.ValidationError(
                'Logged In User required'
            )
        positions = validated_data.pop('positions')
        validated_data['owner'] = owner
        site_project = models.SiteProject.objects.create(**validated_data)
        for position in positions:
            models.Position.objects.create(project=site_project, **position)
        return site_project


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Position
        fields = ['title', 'description', 'status', 'applicant', 'project',
                  'skill']