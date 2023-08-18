"""Course views."""

# from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Course


class OwnerMixin(object):
    """Owner mixin."""

    def get_queryset(self):
        """Retrieve owner object."""
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)


class OwnerEditMixin(object):
    """Owner edit mixin."""

    def form_valid(self, form):
        """
        Validate owner form edit.

        Args:
            form: Owner form instance.
        """
        form.instance.owner = self.request.user
        return super().form_valid(form)


class OwnerCourseMixin(OwnerMixin, LoginRequiredMixin, PermissionRequiredMixin):
    """Owner course mixin."""

    model = Course
    fields = ['subject', 'title', 'slug', 'overview']
    success_url = reverse_lazy('manage_course_list')


class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    """Owner course edit mixin."""

    template_name = 'courses/manage/course/form.html'


class ManageCourseListView(OwnerCourseMixin, ListView):
    """Course list view manager view."""

    template_name = "courses/manage/course/list.html"
    permission_required = 'courses.view_course'


class CourseCreateView(OwnerCourseEditMixin, CreateView):
    """Course create view."""

    permission_required = 'courses.view_course'


class CourseUpdateView(OwnerCourseEditMixin, UpdateView):
    """Course update view."""

    permission_required = 'courses.view_course'


class CourseDeleteView(OwnerCourseEditMixin, DeleteView):
    """Course delete view."""

    template_name = 'courses/manage/course/delete.html'
    permission_required = 'courses.view_course'
