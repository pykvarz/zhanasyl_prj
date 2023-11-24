
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView

from django.shortcuts import redirect
from django.urls import reverse_lazy

from django.views.generic import CreateView, TemplateView, FormView

from users.forms import CustomUserCreationForm, CheckKeyForm
from users.mixins import GroupRequiredMixin, PermRequiredMixin
from users.models import CustomUser
from users.service import add_perm, check_key

import logging

logger = logging.getLogger(__name__)


# Create your views here.

class CustomUserCreateView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'register.html'
    success_url = '/user/login/'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect("dashboard")
        return super().dispatch(request, *args, **kwargs)


class CustomUserLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'login.html'


class DashboardView(GroupRequiredMixin, TemplateView):
    group_id = 3
    template_name = 'dashboard.html'


class AddPermView(LoginRequiredMixin, PermRequiredMixin, FormView):
    template_name = 'check_code.html'
    form_class = CheckKeyForm
    success_url = reverse_lazy('dashboard')
    group_id = 3

    def form_valid(self, form):
        key = form.cleaned_data['key']
        if check_key(key=key):
            add_perm(user_id=self.request.user.id, group_id=self.group_id)
            return super().form_valid(form)
        else:
            return self.form_invalid(form)


class TestView(TemplateView):
    template_name = 'test.html'
