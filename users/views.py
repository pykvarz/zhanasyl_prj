from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import CreateView, TemplateView, FormView

from users.forms import CustomUserCreationForm, CheckKeyForm
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


@method_decorator(permission_required('users.view_dashboard', login_url="/user/check"), name='dispatch')
class DashboardView(TemplateView):
    template_name = 'dashboard.html'


class AddPermView(LoginRequiredMixin, UserPassesTestMixin, FormView):
    template_name = 'check_code.html'
    form_class = CheckKeyForm
    success_url = reverse_lazy('dashboard')

    def test_func(self):
        return not self.request.user.user_permissions.filter(pk=32).exists()

    def handle_no_permission(self):
        return HttpResponseRedirect(self.success_url)

    def form_valid(self, form):
        key = form.cleaned_data['key']
        if check_key(key=key):
            add_perm(user_id=self.request.user.id, p_id=32)
            return super().form_valid(form)
        else:
            return self.form_invalid(form)


class TestView(TemplateView):
    template_name = 'test.html'
