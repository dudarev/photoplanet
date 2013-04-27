from django.views.generic import TemplateView


class LoginView(TemplateView):
    template_name = "users/login.html"


class LoginErrorView(TemplateView):
    template_name = "users/login-error.html"
