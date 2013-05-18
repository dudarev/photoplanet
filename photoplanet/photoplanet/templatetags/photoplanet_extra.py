"""
Custom template tag to show date. Taken from

https://docs.djangoproject.com/en/1.5/howto/custom-template-tags/
"""
import datetime

from django import template
from django.core.urlresolvers import reverse


INSTAGRAM_USER_URL_TEMPLATE = 'http://instagram.com/{}'

register = template.Library()


@register.simple_tag
def current_time(format_string):
    return datetime.datetime.now().strftime(format_string)


@register.simple_tag
def url_for_today():
    d = datetime.date.today()
    return reverse('photo-date-view', kwargs={'year': d.year, 'month': d.month, 'day': d.day})


@register.simple_tag
def instagram_url(username):
    return INSTAGRAM_USER_URL_TEMPLATE.format(username)
