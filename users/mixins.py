from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views import View
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from users.models import Object

class IsSuperUserClass:
    def is_super_user(self):
        return self.request.user.is_superuser


class InGroupRequiredMixin(UserPassesTestMixin, IsSuperUserClass, View):
    group_id = None  # Укажите имя группы в подклассе
    success_url = None


    def test_func(self):
        return not self.is_super_user() or self.request.user.groups.filter(pk=self.group_id).exists()

    def handle_no_permission(self):
        return HttpResponseRedirect(self.success_url)


class NotPermRequiredMixin(UserPassesTestMixin):
    group_id = None
    success_url = None

    def test_func(self):
        """
        Метод, выполняющий пользовательский тест для проверки прав доступа.
        Если метод возвращает True, то доступ разрешен, если False - доступ запрещен.
        В данном случае, тест проверяет, что пользователь **не** принадлежит группе с идентификатором self.group_id.
        """
        return not self.request.user.groups.filter(pk=self.group_id).exists() or self.request.user.is_superuser

    def handle_no_permission(self):
        return HttpResponseRedirect(self.success_url)


class MyLoginPermissionRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy("login"))
        return super().dispatch(request, *args, **kwargs)


class MyMixin(IsSuperUserClass, UserPassesTestMixin):

    def test_func(self):
        return self.is_super_user() or self.get_object().users.filter(pk=self.request.user.pk).exists()
    def handle_no_permission(self):
        raise Http404







