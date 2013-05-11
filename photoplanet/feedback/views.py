from django import forms
from django.views.generic import CreateView
from django.core.urlresolvers import reverse_lazy

from braces.views import LoginRequiredMixin

from .models import Feedback


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        exclude = ('user', )


class FeedbackCreateView(LoginRequiredMixin, CreateView):
    model = Feedback
    form_class = FeedbackForm
    template_name = 'feedback/feedback.html'
    # https://docs.djangoproject.com/en/1.5/topics/class-based-views/generic-editing/#model-forms
    success_url = reverse_lazy('home')
    
    # https://docs.djangoproject.com/en/1.5/topics/class-based-views/generic-editing/
    # #models-and-request-user
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(FeedbackCreateView, self).form_valid(form)
