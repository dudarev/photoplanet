from django.conf import settings


# https://docs.djangoproject.com/en/dev/ref/templates/api/#writing-your-own-context-processors
def extra(request):
    return {
        'CUSTOM_HEADLINE': settings.CUSTOM_HEADLINE,
        'INCLUDE_ANALYTICS': settings.INCLUDE_ANALYTICS,
    }
