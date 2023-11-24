from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, TemplateView, FormView

from users.decorators import has_key_user_required
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


# @method_decorator(permission_required('users.view_dashboard', login_url="/user/check"), name='dispatch')
class DashboardView(GroupRequiredMixin, TemplateView):
    group_id = 3
    template_name = 'dashboard.html'

    # def test_func(self):
    #     return not self.request.user.groups.filter(pk=3)
    #
    # def handle_no_permission(self):
    #     return HttpResponseRedirect(reverse_lazy('check'))


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
