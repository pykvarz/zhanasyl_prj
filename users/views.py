from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.views.generic import CreateView, TemplateView

from users.forms import CustomUserCreationForm
from users.models import CustomUser


# Create your views here.

class CustomUserCreateView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'register.html'
    success_url = 'user/login/'  # Замените '/success/' на ваш URL успешного создания объекта


class CustomUserLoginView(LoginView):
    template_name = 'login.html'
    success_url = 'user/dashboard/'


class DashboardView(TemplateView):
    template_name = 'dashboard.html'
