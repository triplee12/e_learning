"""Course views."""

from django.apps import apps
from django.db.models import Count
from django.shortcuts import redirect, get_object_or_404
from django.forms.models import modelform_factory
from django.urls import reverse_lazy
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.cache import cache
from braces.views import CsrfExemptMixin, JsonRequestResponseMixin
from students.forms import CourseEnrollForm
from .models import Course, Content, Module, Subject
from .forms import ModuleFormSet


class CourseModuleUpdateView(TemplateResponseMixin, View):
    """Course module update view."""

    template_name = 'courses/manage/module/formset.html'
    course = None

    def get_formset(self, data=None):
        """Get the formset."""
        return ModuleFormSet(instance=self.course, data=data)

    def dispatch(self, request, pk):
        """Dispatch the request."""
        self.course = get_object_or_404(
            Course, id=pk, owner=request.user
        )
        return super().dispatch(request, pk)

    def get(self, request, *args, **kwargs):
        """Get the course formset."""
        formset = self.get_formset()
        return self.render_to_response(
            {'course': self.course, 'formset': formset}
        )

    def post(self, request, *args, **kwargs):
        """Post a course module."""
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('manage_course_list')
        return self.render_to_response(
            {'course': self.course, 'formset': formset}
        )


class ContentCreateUpdateView(TemplateResponseMixin, View):
    """Content Update view for creating module."""

    module = None
    model = None
    obj = None
    template_name = 'courses/manage/content/form.html'

    def get_model(self, model_name):
        """Get the model."""
        if model_name in ['text', 'video', 'image', 'file']:
            return apps.get_model(app_label='courses', model_name=model_name)
        return None

    def get_form(self, model, *args, **kwargs):
        """Get the form."""
        form = modelform_factory(
            model, exclude=[
                'owner', 'order',
                'created', 'updated'
            ]
        )
        return form(*args, **kwargs)

    def dispatch(self, request, module_id, model_name, id=None):
        """Dispatch a request."""
        self.module = get_object_or_404(
            Module, id=module_id,
            course__owner=request.user
        )
        self.model = self.get_model(model_name)
        if id:
            self.obj = get_object_or_404(
                self.model, id=id,
                owner=request.user
            )
        return super().dispatch(request, module_id, model_name, id)

    def get(self, request, module_id, model_name, id=None):
        """Get a model from request."""
        form = self.get_form(self.model, instance=self.obj)
        return self.render_to_response({
            'form': form,
            'object': self.obj
        })

    def post(self, request, module_id, model_name, id=None):
        """Post a model form."""
        form = self.get_form(
            self.model, instance=self.obj,
            data=request.POST,
            files=request.FILES
        )
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            if not id:
                # New content
                Content.objects.create(module=self.module, item=obj)
            return redirect('module_content_list', self.module.id)
        return self.render_to_response({'form': form, 'object': self.obj})


class ContentOrderView(CsrfExemptMixin, JsonRequestResponseMixin, View):
    """Content Order View."""

    def post(self, request):
        """Post request to order content."""
        for id, order in self.request_json.items():
            Content.objects.filter(
                id=id, module__course__owner=request.user
            ).update(order=order)
        return self.render_json_response({"saved": "OK"})


class ModuleContentListView(TemplateResponseMixin, View):
    """Module content list view."""

    template_name = 'courses/manage/module/content_list.html'

    def get(self, request, module_id):
        """Get a list of content."""
        module = get_object_or_404(
            Module, id=module_id,
            course__owner=request.user
        )
        return self.render_to_response({'module': module})


class ModuleOrderView(CsrfExemptMixin, JsonRequestResponseMixin, View):
    """Module order view."""

    def post(self, request):
        """Post a request to order the module."""
        for id, order in self.request_json.items():
            Module.objects.filter(
                id=id, course__owner=request.user
            ).update(order=order)
        return self.render_json_response({'saved': 'OK'})


class ContentDeleteView(View):
    """Content Delete View."""

    def post(self, request, id):
        """Post a delete request."""
        content = get_object_or_404(
            Content, id=id,
            module__course__owner=request.user
        )
        module = content.module
        content.item.delete()
        content.delete()
        return redirect('module_content_list', module.id)


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


class CourseListView(TemplateResponseMixin, View):
    """Course list view."""

    model = Course
    template_name = 'courses/course/list.html'

    def get(self, request, subject=None):
        """Get a list of courses."""
        subjects = cache.get("all_subjects")
        if not subjects:
            subjects = Subject.objects.annotate(
                total_coueses=Count('courses')
            )
            cache.set("all_subjects", subjects)
        all_courses = Course.objects.annotate(
            total_modules=Count('modules')
        )
        if subject:
            subject = get_object_or_404(Subject, slug=subject)
            key = f'subject_{subject.id}_courses'
            courses = cache.get(key)
            if not courses:
                courses = all_courses.filter(subject=subject)
                cache.set(key, courses)
        else:
            courses = cache.get('all_courses')
            if not courses:
                courses = all_courses
                cache.set('all_courses', courses)
        return self.render_to_response(
            {
                'subject': subject,
                'subjects': subjects,
                'courses': courses
            }
        )


class CourseDetailView(DetailView):
    """Course Detail view."""

    model = Course
    template_name = "courses/course/detail.html"

    def get_context_data(self, **kwargs):
        """Get the context data."""
        context = super().get_context_data(**kwargs)
        context['enroll_form'] = CourseEnrollForm(
            initial={'course': self.object}
        )
        return context
