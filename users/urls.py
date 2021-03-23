from django.urls import path
from django.contrib.auth import views as auth_views
from users.views import UserCreateView

urlpatterns = [
    path('sign-up/', UserCreateView.as_view(), name="create-user"),
    path('', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
