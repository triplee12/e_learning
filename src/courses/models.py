"""Courses model."""

from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.template.loader import render_to_string
from .fields import OrderField


class Subject(models.Model):
    """Subject model."""

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        """Subject meta details."""

        ordering = ['title']

    def __str__(self):
        """Subject string representation."""
        return f'{self.title}'


class Course(models.Model):
    """Course model."""

    owner = models.ForeignKey(
        User, related_name='courses_created',
        on_delete=models.CASCADE
    )
    subject = models.ForeignKey(
        Subject, related_name='courses',
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    overview = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    students = models.ManyToManyField(User, related_name="courses_joined", blank=True)

    class Meta:
        """Course meta details."""

        ordering = ['-created']

    def __str__(self):
        """Course string representation."""
        return f'{self.title}'


class Module(models.Model):
    """Module model."""

    course = models.ForeignKey(
        Course, related_name='modules',
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = OrderField(blank=True, for_fields=['course'])

    class Meta:
        """Module meta details."""

        ordering = ['order']

    def __str__(self):
        """Module string representation."""
        return f"{self.order}. {self.title}"


class Content(models.Model):
    """Content model."""

    module = models.ForeignKey(
        Module, related_name="contents",
        on_delete=models.CASCADE
    )
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE,
        limit_choices_to={
            'model__in': (
                'text',
                'video',
                'image',
                'file'
            )
        }
    )
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    order = OrderField(blank=True, for_fields=['module'])

    class Meta:
        """Conent meta details."""

        ordering = ['order']


class ItemBase(models.Model):
    """Item base model."""

    owner = models.ForeignKey(
        User, related_name='%(class)s_related',
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        """Meta details for item base model."""

        abstract = True

    def __str__(self):
        """Item base model string representation."""
        return f"{self.title}"

    def render(self):
        """Render items."""
        return render_to_string(
            f'courses/content/{self._meta.model_name}.html',
            {'item': self}
        )


class Text(ItemBase):
    """Text base model."""

    content = models.TextField()


class File(ItemBase):
    """File base model."""

    file = models.FileField(upload_to='files')


class Image(ItemBase):
    """Image base model."""

    file = models.FileField(upload_to='images')


class Video(ItemBase):
    """Video base model."""

    url = models.URLField()
