"""Courses api serializers."""

from rest_framework import serializers
from ..models import Subject, Course, Module


class SubjectSerializer(serializers.ModelSerializer):
    """Subject serializer."""

    class Meta:
        """Meta class for Subject instances."""

        model = Subject
        fields = ['id', 'title', 'slug']


class ModuleSerializer(serializers.ModelSerializer):
    """Module serializer."""

    class Meta:
        """Meta class for Module instances."""

        model = Module
        fields = ['order', 'title', 'description']


class CourseSerializer(serializers.ModelSerializer):
    """Course serializer."""

    modules = ModuleSerializer(many=True, read_only=True)

    class Meta:
        """Meta class for Course instances."""

        model = Course
        fields = [
            'id', 'title', 'slug', 'overview',
            'subject', 'created', 'owner', 'modules'
        ]
