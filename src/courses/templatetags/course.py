"""Course template tags."""

from django import template

register = template.Library()


@register.filter
def model_name(obj):
    """Model name template tag."""
    try:
        return obj._meta.model_name
    except AttributeError:
        return None
