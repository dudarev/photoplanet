from django.views.generic import TemplateView


class LoginView(TemplateView):
    template_name = "users/login.html"

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        context['next'] = self.request.GET.get('next', None)
        return context


class LoginErrorView(TemplateView):
    template_name = "users/login-error.html"
