"""Courses api serializers."""

from rest_framework import serializers
from ..models import Subject, Course, Module, Content


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


class ItemRelatedField(serializers.RelatedField):
    """Item related field."""

    def to_representation(self, value):
        """To represent the value of this field."""
        return value.render()


class ContentSerializer(serializers.ModelSerializer):
    """Content serializer."""

    item = ItemRelatedField(read_only=True)

    class Meta:
        """Meta class for ContentSerializer."""

        model = Content
        fields = ['order', 'item']


class ModuleWithContentsSerializer(serializers.ModelSerializer):
    """Module with content serializer."""

    contents = ContentSerializer(many=True)
    
    class Meta:
        """Meta class for module with content serializer."""

        model = Module
        fields = [
            'order', 'titles',
            'description', 'contents'
        ]


class CourseWithContentsSerializer(serializers.ModelSerializer):
    """Course with contents serializer."""

    modules = ModuleWithContentsSerializer(many=True)

    class Meta:
        """Meta class for CourseWithContentsSerializer."""

        model = Course
        fields = [
            'id', 'title', 'slug', 'overview',
            'subject', 'created', 'owner', 'modules'
        ]
