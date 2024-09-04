from rest_framework_simplejwt.views import TokenRefreshView

from django.urls import path

from common.auth.views import (
    LoginView,
    RegisterView,
    VerifyEmailView,
    PasswordResetVerifyCodeView,
    PasswordResetChangeView,
    PasswordResetView,
)


urlpatterns = [
    path("registration/", RegisterView.as_view(), name="registration"),
    path("verify-email/", VerifyEmailView.as_view(), name="verify-email"),
    path("login/", LoginView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("password/reset/", PasswordResetView.as_view(), name="password_reset"),
    path(
        "password/reset/verify/",
        PasswordResetVerifyCodeView.as_view(),
        name="password_reset_verify",
    ),
    path(
        "password/reset/change/",
        PasswordResetChangeView.as_view(),
        name="password_reset_change",
    ),
]
