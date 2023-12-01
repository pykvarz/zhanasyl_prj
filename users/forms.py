from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import CustomUser, Object


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name']


class CustomUserAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']


class CheckKeyForm(forms.Form):
    key = forms.CharField(label='key', max_length=100)


class CreateObjectForm(forms.ModelForm):
    class Meta:
        model = Object
        fields = ["name"]


class ObjectUpdateForm(forms.ModelForm):
    class Meta:
        model = Object
        fields = ["name"]


class ObjectCreateForm(forms.ModelForm):
    class Meta:
        model = Object
        fields = ["name"]
