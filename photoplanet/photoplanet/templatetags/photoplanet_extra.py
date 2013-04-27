"""
Custom template tag to show date. Taken from

https://docs.djangoproject.com/en/1.5/howto/custom-template-tags/
"""
import datetime

from django import template


register = template.Library()


@register.simple_tag
def current_time(format_string):
    return datetime.datetime.now().strftime(format_string)
