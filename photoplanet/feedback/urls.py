from django.conf.urls import patterns, url
from feedback.views import FeedbackView

urlpatterns = patterns(
    '',
    url(
        r'^$',
        FeedbackView.as_view(),
        name='feedback')
)
