"""Views for the chats."""

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required


@login_required
def course_chat_room(request, course_id):
    """Course chat room."""
    try:
        # Retrieve course with the given id joined by the user
        course = request.user.courses_joined.get(
            id=course_id
        )
    except:
        # User is not a student of the course
        # or the course does not exist
        return HttpResponseForbidden()
    return render(request, 'chats/room.html', {'course': course})
