"""Stusents view."""

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, FormView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from courses.models import Course
from .forms import CourseEnrollForm


class StudentRegistrationView(CreateView):
    """Student registration view."""

    template_name = "students/student/registration.html"
    form_class = UserCreationForm
    success_url = reverse_lazy('student_course_list')

    def form_valid(self, form):
        """Validate the form.

        Args:
            form: Form to be validated
        """
        result = super().form_valid(form)
        cd = form.cleaned_data
        user = authenticate(
            username=cd['username'],
            password=cd['password']
        )
        login(self.request, user)
        return result


class StudentEnrollCourseView(LoginRequiredMixin, FormView):
    """Student course enrollment view."""

    course = None
    form_class = CourseEnrollForm

    def form_valid(self, form):
        """Validate the form."""
        self.course = form.cleaned_data['course']
        self.course.students.add(self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        """Get the URL to redirect."""
        return reverse_lazy(
            'student_course_detail',
            args=[self.course.id]
        )


class StudentCourseListView(LoginRequiredMixin, ListView):
    """Student Course List view."""

    model = Course
    template_name = 'students/course/list.html'

    def get_queryset(self):
        """Get the list of courses the user has access to."""
        qs = super().get_queryset()
        return qs.filter(students__in=[self.request.user])


class StudentCourseDetailView(DetailView):
    """Student Course Detail view."""

    model = Course
    template_name = "students/course/detail.html"

    def get_queryset(self):
        """Get details of a course the student enrolled on."""
        qs = super().get_queryset()
        return qs.filter(students__in=[self.request.user])

    def get_context_data(self, **kwargs):
        """Get the context data."""
        context = super().get_context_data(**kwargs)
        # Get course objects
        course = self.get_object()
        if 'module_id' in self.kwargs:
            # Get current module
            context['module'] = course.modules.get(
                id=self.kwargs['module_id']
            )
        else:
            # Get first module
            context['module'] = course.modules.all()[0]
        return context
