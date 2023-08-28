"""Middleware for accessing course subdomain."""

from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect
from .models import Course


def subdomain_course_middleware(get_response):
    """Subdomain middleware for courses."""
    def middleware(request):
        """Middleware for courses."""
        host_parts = request.het_host().split('.')
        if len(host_parts) > 2 and host_parts[0] != 'www':
            # Get course for the given subdomain
            course = get_object_or_404(Course, slug=host_parts[0])
            course_url = reverse('course_detail', args=[course.slug])
            # redirect current request to the course detail
            url = '{}://{}{}'.format(
                request.scheme, '.'.join(host_parts[1:]),
                course_url
            )
            return redirect(url)
        response = get_response(request)
        return response
    return middleware
