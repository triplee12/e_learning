"""Course admin site."""

from django.contrib import admin
from .models import Course, Module, Subject

# use memcache admin index site
admin.site.index_template = 'memcache_status/admin_index.html'


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    """Subject admin site."""

    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}


class ModuleInline(admin.StackedInline):
    """Module inlined."""

    model = Module


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """Course admin site."""

    list_display = ['title', 'slug', 'created']
    list_filter = ['created', 'subject']
    search_fields = ['title', 'overview']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ModuleInline]
