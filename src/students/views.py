"""Stusents view."""

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, FormView
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
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
