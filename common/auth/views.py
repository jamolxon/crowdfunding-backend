from rest_framework.authtoken.views import ObtainAuthToken

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView as TokenObtainView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, GenericAPIView, UpdateAPIView
from rest_framework import status

from django.utils import timezone
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail


from allauth.account.adapter import get_adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.views import LoginView as RestLoginView


from common.models import User

from .serializers import (
    TokenObtainLoginSerializer,
    RegisterSerializer,
    VerifyEmailSerializer,
    UserPasswordResetSerializer,
    PasswordResetChangeSerializer,
    PasswordResetVerifyCodeSerializer,
    SocialLoginSerializer
)
from .exceptions import UserLoggedIn
from .utils import generate_pin


class RegisterView(ObtainAuthToken, CreateAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        """
        Register API
        """
        if request.user.is_authenticated:
            raise UserLoggedIn(_("Allaqachon tizimga kirgansiz."))

        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        if user.code_expiration < timezone.now() - timezone.timedelta(
            minutes=settings.REGISTRATION_EXPIRATION_CODE_MINUTES
        ):  # noqa
            user.code = generate_pin()
            user.code_expiration = timezone.now()
            user.save(update_fields=["code", "code_expiration"])

        send_mail(
            "Crowdfunding registration confirmation code.",
            f"Thanks for registering on our platform. Your code is {user.code}",
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False
        )

        # send_email_confirmation(
        #     email=user.email,
        #     code=user.code,
        #     domain=settings.HOST,
        #     uid=urlsafe_base64_encode(force_bytes(user.pk)),
        #     token=account_activation_token.make_token(user),
        # )

        return Response(serializer.data, status=status.HTTP_200_OK)


class VerifyEmailView(GenericAPIView):
    serializer_class = VerifyEmailSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):  # noqa
        """
        Email verification API
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user

        if not user.is_active:
            user.is_active = True
            user.code = User.INVALID_CODE
            user.save(update_fields=["is_active", "code"])

        refresh = RefreshToken.for_user(user)

        return Response({"refresh": str(refresh), "access": str(refresh.access_token)})


class LoginView(TokenObtainView):
    """
    Login API
    """

    permission_classes = (AllowAny,)
    serializer_class = TokenObtainLoginSerializer


class PasswordResetView(GenericAPIView):
    serializer_class = UserPasswordResetSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):  # noqa
        """
        Password Reset
        """

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()  # noqa

        try:
            user = User.objects.get(email=user.email)
        except User.DoesNotExist:  # noqa
            raise NotFound(_("Foydalanuvchi topilmadi."))  # noqa

        if user.code_expiration < timezone.now() - timezone.timedelta(
            minutes=settings.REGISTRATION_EXPIRATION_CODE_MINUTES
        ):  # noqa
            user.code = generate_pin()
            user.code_expiration = timezone.now()
            user.save(update_fields=["code", "code_expiration"])
    
        send_mail(
            "Crowdfunding password reset confirmation code.",
            f"Your code is {user.code}",
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False
        )


            # send_email_restore_password(
            #     email=user.email,
            #     code=user.code,
            #     domain=settings.HOST,
            #     uid=urlsafe_base64_encode(force_bytes(user.pk)),
            #     token=account_activation_token.make_token(user),
            # )
        return Response(serializer.data, status=status.HTTP_200_OK)


class PasswordResetVerifyCodeView(GenericAPIView):
    serializer_class = PasswordResetVerifyCodeSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):  # noqa
        """
        Password Reset verification
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.user
        user.code = User.INVALID_CODE
        user.save()

        refresh = RefreshToken.for_user(user)

        return Response({"refresh": str(refresh), "access": str(refresh.access_token)})


class PasswordResetChangeView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = PasswordResetChangeSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        """
        Password Update
        """
        user = self.get_object()

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Set new password for user
        user.set_password(serializer.validated_data.get("new_password"))
        user.save()

        return Response(
            {"detail": "Parol muvaffaqiyatli o'zgartirildi."}, status=status.HTTP_200_OK
        )


class SocialLoginView(RestLoginView):
    serializer_class = SocialLoginSerializer

    def process_login(self):
        get_adapter(self.request).login(self.request, self.user)


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = settings.OAUTH_CALLBACK_URL
    client_class = OAuth2Client

