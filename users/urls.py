from django.contrib.auth.views import LogoutView
from django.urls import path
from users.views import CustomUserCreateView, CustomUserLoginView, DashboardView, AddPermView, TestView, \
    CreateObjectView, ObjectDetailView, ObjectDeleteView, ObjectUpdateView, ObjectCreateView

urlpatterns = [
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', CustomUserCreateView.as_view(), name='register'),
    path('login/', CustomUserLoginView.as_view(), name='login'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('check/', AddPermView.as_view(), name='check'),
    path('test/', TestView.as_view(), name='test'),
    path('create/', CreateObjectView.as_view(), name='create'),
    path('detail/<int:pk>', ObjectDetailView.as_view(), name='object_detail'),
    path(',<int:pk>/delete/', ObjectDeleteView.as_view(), name='object_delete'),
    path('update/<int:pk>', ObjectUpdateView.as_view(), name='object_update'),
    path('create/', ObjectCreateView.as_view(), name='object_create'),

]
