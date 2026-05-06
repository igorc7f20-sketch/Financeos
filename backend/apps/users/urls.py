from django.urls import path
from .views import RegisterView, ProfileView, LoginView, RefreshTokenView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="auth-register"),
    path("login/", LoginView.as_view(), name="auth-login"),
    path("profile/", ProfileView.as_view(), name="auth-profile"),
    path("refresh/", RefreshTokenView.as_view(), name="auth-refresh"),
]
