"""Students form."""

from django import forms
from courses.models import Course


class CourseEnrollForm(forms.Form):
    """Course enrollment form."""

    course = forms.ModelChoiceField(
        queryset=Course.objects.all(),
        widget=forms.HiddenInput
    )
