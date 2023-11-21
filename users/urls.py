from django.urls import path
from .views import CustomUserCreateView, CustomUserLoginView, DashboardView, AddPermView

urlpatterns = [
    path('register/', CustomUserCreateView.as_view(), name='register'),
    path('login/', CustomUserLoginView.as_view(), name='login'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('check/', AddPermView.as_view(), name='check'),
]
