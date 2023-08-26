"""Courses api permission."""

from rest_framework.permissions import BasePermission


class IsEnrolled(BasePermission):
    """Is the user enrolled."""

    def has_object_permission(self, request, view, obj):
        """Check if the user has an object permission."""
        return obj.students.filter(id=request.user.id).exists()
