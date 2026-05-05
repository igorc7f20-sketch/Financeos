from django.urls import path
from .views import RegisterView, ProfileView, LoginView, RefreshView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="auth-register"),
    path("login/", LoginView.as_view(), name="auth-login"),
    path("profile/", ProfileView.as_view(), name="auth-profile"),
    path("refresh/", RefreshView.as_view(), name="auth-refresh"),
]