"""Courses api views."""

from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Subject, Course
from .serializers import SubjectSerializer, CourseSerializer


class SubjectListView(generics.ListAPIView):
    """Subject list view."""

    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class SubjectDetailView(generics.RetrieveAPIView):
    """Subject detail view."""

    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


# class CourseEnrollView(APIView):
#     """Course enrollment view."""

#     authentication_classes = (BasicAuthentication,)
#     permission_classes = (IsAuthenticated,)

#     def post(self, request, pk, format=None):
#         """Post course enrollment."""
#         course = get_object_or_404(Course, pk=pk)
#         course.students.add(request.user)
#         return Response({"enrolled": True})


class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    """Course view set."""

    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    @action(
        detail=['post'],
        authentication_classes=[BasicAuthentication],
        permission_classes=[IsAuthenticated]
    )
    def enroll(self, request, *args, **kwargs):
        """Enroll into the Course."""
        course = self.get_object()
        course.students.add(request.user)
        return Response({"enrolled": True})
