from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import CreateView, TemplateView

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
    success_url = 'user/login/'  # Замените '/success/' на ваш URL успешного создания объекта


class CustomUserLoginView(LoginRequiredMixin, LoginView):
    template_name = 'login.html'
    login_url = '/user/dashboard/'

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect('/user/dashboard')




@method_decorator(permission_required('users.view_dashboard'), name='dispatch')
class DashboardView(TemplateView):
    template_name = 'dashboard.html'


class AddPermView(LoginRequiredMixin, View):
    template_name = 'check_code.html'

    def get(self, request):
        form = CheckKeyForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = CheckKeyForm(request.POST)
        if form.is_valid():
            key = form.cleaned_data['key']
            # result = check_key(key="534d66eeaff3edd6e0b1008139dac451e265c5390eb10db5a4c9311fef2d8466")
            # logger.info(result)
            # return HttpResponse(result)
            if check_key(key=key):
                add_perm(user_id=request.user.id, p_id=32)
                return HttpResponseRedirect('/user/dashboard/')
            else:
                return render(request, self.template_name, {"form": form})
        return render(request, self.template_name, {"form": form})
