"""
Custom template tag to show date. Taken from

https://docs.djangoproject.com/en/1.5/howto/custom-template-tags/
"""
import datetime

from django import template


INSTAGRAM_USER_URL_TEMPLATE = 'http://instagram.com/{}'

register = template.Library()


@register.simple_tag
def current_time(format_string):
    return datetime.datetime.now().strftime(format_string)

@register.simple_tag
def instagram_url(username):
    return INSTAGRAM_USER_URL_TEMPLATE.format(username)
