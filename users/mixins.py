from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views import View
from django.http import HttpResponseRedirect


class GroupRequiredMixin(UserPassesTestMixin, View):
    group_id = None  # Укажите имя группы в подклассе

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.groups.filter(pk=self.group_id)

    def handle_no_permission(self):
        return HttpResponseRedirect(reverse_lazy('check'))


class PermRequiredMixin(UserPassesTestMixin, View):
    group_id = None
    success_url = None

    def test_func(self):
        """
        Метод, выполняющий пользовательский тест для проверки прав доступа.
        Если метод возвращает True, то доступ разрешен, если False - доступ запрещен.
        В данном случае, тест проверяет, что пользователь **не** принадлежит группе с идентификатором self.group_id.
        """
        return not self.request.user.is_superuser or self.request.user.groups.filter(pk=self.group_id).exists()

    def handle_no_permission(self):
        return HttpResponseRedirect(self.success_url)

