"""Courses api views."""

from rest_framework import generics
from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
# from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Subject, Course
from .permissions import IsEnrolled
from .serializers import (
    SubjectSerializer, CourseSerializer,
    CourseWithContentsSerializer
)


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
        detail=True,
        methods=['post'],
        authentication_classes=[BasicAuthentication],
        permission_classes=[IsAuthenticated]
    )
    def enroll(self, request, *args, **kwargs):
        """Enroll into the Course."""
        course = self.get_object()
        course.students.add(request.user)
        return Response({"enrolled": True})

    @action(
        detail=True,
        methods=['get'],
        serializer_class=CourseWithContentsSerializer,
        authentication_classes=[BasicAuthentication],
        permission_classes=[IsAuthenticated, IsEnrolled]
    )
    def contents(self, request, *args, **kwargs):
        """Content of the course."""
        return self.retrieve(request, *args, **kwargs)
