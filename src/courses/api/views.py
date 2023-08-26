"""Courses api views."""

from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Subject, Course
from .serializers import SubjectSerializer


class SubjectListView(generics.ListAPIView):
    """Subject list view."""

    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class SubjectDetailView(generics.RetrieveAPIView):
    """Subject detail view."""

    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class CourseEnrollView(APIView):
    """Course enrollment view."""

    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk, format=None):
        """Post course enrollment."""
        course = get_object_or_404(Course, pk=pk)
        course.students.add(request.user)
        return Response({"enrolled": True})
