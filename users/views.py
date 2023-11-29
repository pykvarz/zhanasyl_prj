from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect, Http404

from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy

from django.views.generic import CreateView, TemplateView, FormView, ListView, DetailView

from users.forms import CustomUserCreationForm, CheckKeyForm, CreateObjectForm
from users.mixins import InGroupRequiredMixin, NotPermRequiredMixin, \
    MyLoginPermissionRequiredMixin, MyMixin
from users.models import CustomUser, Object
from users.service import add_perm, check_key

import logging

logger = logging.getLogger(__name__)


# Create your views here.

class CustomUserCreateView(MyLoginPermissionRequiredMixin, CreateView):
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


class DashboardView(MyLoginPermissionRequiredMixin, InGroupRequiredMixin, ListView):
    group_id = 3
    template_name = 'dashboard.html'
    paginate_by = 5
    model = Object
    context_object_name = 'user_products'
    success_url = reverse_lazy("check")

    def get_queryset(self):
        return Object.objects.filter(users=self.request.user.id)


class AddPermView(MyLoginPermissionRequiredMixin, NotPermRequiredMixin, FormView):
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


class CreateObjectView(MyLoginPermissionRequiredMixin, FormView):
    model = Object
    template_name = "create.html"
    form_class = CreateObjectForm
    success_url = '/user/dashboard/'

    def form_valid(self, form):
        object = form.save()
        object.users.add(self.request.user)
        return super().form_valid(form)


class ObjectDetailView(MyLoginPermissionRequiredMixin, MyMixin, DetailView):
    model = Object
    template_name = 'object_detail.html'
    context_object_name = 'object'

    # def test_func1(self):
    #     if self.get_object() is not None:
    #         if self.request.user in self.get_object().users.all():
    #             return HttpResponseRedirect(reverse_lazy("dashboard"))
    #     else:
    #         return HttpResponseRedirect(reverse_lazy("dashboard"))
    #
    # def handle_no_permission(self):
    #     return HttpResponseRedirect(reverse_lazy("dashboard"))
