from allauth.account import app_settings as allauth_settings
from allauth.socialaccount.helpers import complete_social_login

from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer as TokenObtainSerializer,
)
from rest_framework import serializers

from django.core.signing import BadSignature
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.password_validation import validate_password
from django.http import HttpRequest
from django.contrib.auth import get_user_model

from common.models import User
from .utils import decode_uid_signature, generate_pin, sign_uid


class TokenObtainLoginSerializer(TokenObtainSerializer):  # noqa
    username_field = User.EMAIL_FIELD
    default_error_messages = {"user_not_found": _("Foydalanuvchi topilmadi.")}

    @classmethod
    def get_token(cls, user):
        print(user)
        token = super().get_token(user)
        try:
            if user:
                return token
            else:
                raise AuthenticationFailed("user_not_found")
        except Exception:
            raise AuthenticationFailed("user_not_found")


class RegisterSerializer(serializers.Serializer):  # noqa
    default_error_messages = {"already_registered": _("Bunday foydalanuvchi mavjud.")}

    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={"input_type": "password"},
    )

    signature = serializers.SerializerMethodField()

    def get_signature(self, obj):  # noqa
        # Return signature
        return sign_uid(obj.id)

    def validate_email(self, email):
        # Raise error if user has registered with this email before
        try:
            user = User.objects.get(email=email.lower())
            self.user = user  # noqa

            if user and user.is_active:
                self.fail("already_registered")
        except User.DoesNotExist:  # noqa
            self.user = None  # noqa
        return email.lower()

    def create(self, validated_data):
        # Return unverified & inactive user
        if self.user:  # noqa
            return self.user  # noqa
        code = generate_pin()
        # Create deactivated user
        user = User.objects.create_user(
            email=validated_data["email"].lower(),
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            password=validated_data["password"],
            code=code,
            is_active=False,
        )

        return user


class VerifyEmailSerializer(serializers.Serializer):  # noqa
    default_error_messages = {
        "code_expired": _("Tasdiqlash kodi vaqti tugati, Qaytadan urinib ko'ring."),
        "invalid_code": _("Kod xato. Qaytadan urinib ko'ring"),
        "invalid_signature": _("Qurilma tasdiqlashda xatolik"),
        "already_registered": _("Bunday foydalanuvchi mavjud."),
    }

    code = serializers.CharField(write_only=True)
    signature = serializers.CharField(write_only=True, max_length=128)

    def validate_signature(self, value):
        # Validate user signature
        try:
            uid = decode_uid_signature(
                value, max_age=settings.REGISTRATION_SEND_CODE_INTERVAL
            )
            self.user = User.objects.get(pk=uid)  # noqa
            return value
        except (BadSignature, User.DoesNotExist):  # noqa
            self.fail("invalid_signature")

    def validate(self, data):
        data = super().validate(data)

        # User has verified activation code before, activation code is no longer valid
        if self.user.code == User.INVALID_CODE:
            self.fail("code_expired")

        # User entered invalid activation code
        # FIXME: invalid code
        if data["code"] != self.user.code:
            self.fail("invalid_code")

        # User is already registered and active
        if self.user.is_active:
            self.fail("already_registered")

        return data


class UserPasswordResetSerializer(serializers.Serializer):  # noqa
    default_error_messages = {"user_not_found": _("Foydalanuvchi topilmadi.")}

    email = serializers.EmailField()
    signature = serializers.SerializerMethodField()

    def get_signature(self, obj):  # noqa
        # Generate new signature for resetting user
        return sign_uid(obj.id)

    def validate_email(self, email):
        # Validate the user email
        try:
            user = User.objects.get(email=email.lower())
            self.user = user  # noqa
        except User.DoesNotExist:  # noqa
            self.fail("user_not_found")

        return email.lower()

    def create(self, validated_data):
        # Return if user exists
        if self.user:
            return self.user
        self.fail("user_not_found")


class PasswordResetVerifyCodeSerializer(serializers.Serializer):  # noqa
    default_error_messages = {
        "code_expired": _("Tasdiqlash kodi vaqti tugati, Qaytadan urinib ko'ring."),
        "invalid_code": _("Kod xato. Qaytadan urinib ko'ring"),
        "invalid_signature": _("Qurilma tasdiqlashda xatolik"),
    }

    code = serializers.CharField(write_only=True)
    signature = serializers.CharField(max_length=128)

    def validate_signature(self, value):  # noqa
        # Validate user signature
        try:
            uid = decode_uid_signature(
                value, max_age=settings.REGISTRATION_SEND_CODE_INTERVAL
            )
            self.user = User.objects.get(pk=uid)  # noqa
            return value
        except (BadSignature, User.DoesNotExist):  # noqa
            self.fail("invalid_signature")

    def validate(self, data):
        data = super().validate(data)

        if self.user.code == User.INVALID_CODE:
            # User has verified activation code before, activation code is no longer valid
            self.fail("code_expired")

        # FIXME: invalid code
        if data["code"] != self.user.code:  # User entered invalid activation code
            self.fail("invalid_code")
        return data


class PasswordResetChangeSerializer(serializers.Serializer):  # noqa
    default_error_messages = {
        "password_mismatch": _("Parollar bir-biriga mos kelmadi.")
    }
    new_password = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )
    password_confirm = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )

    def validate(self, data):
        data = super().validate(data)

        if data["new_password"] != data["password_confirm"]:
            # User entered different passwords
            self.fail("password_mismatch")

        return data


class SocialLoginSerializer(serializers.Serializer):
    access_token = serializers.CharField(required=False, allow_blank=True)
    code = serializers.CharField(required=False, allow_blank=True)

    def _get_request(self):
        request = self.context.get('request')
        if not isinstance(request, HttpRequest):
            request = request._request
        return request

    def get_social_login(self, adapter, app, token, response):
        """
        :param adapter: allauth.socialaccount Adapter subclass.
            Usually OAuthAdapter or Auth2Adapter
        :param app: `allauth.socialaccount.SocialApp` instance
        :param token: `allauth.socialaccount.SocialToken` instance
        :param response: Provider's response for OAuth1. Not used in the
        :returns: A populated instance of the
            `allauth.socialaccount.SocialLoginView` instance
        """
        request = self._get_request()
        social_login = adapter.complete_login(request, app, token, response=response)
        social_login.token = token
        return social_login

    def validate(self, attrs):
        view = self.context.get('view')
        request = self._get_request()

        if not view:
            raise serializers.ValidationError(
                _("View is not defined, pass it as a context variable")
            )

        adapter_class = getattr(view, 'adapter_class', None)
        if not adapter_class:
            raise serializers.ValidationError(_("Define adapter_class in view"))

        adapter = adapter_class(request)
        app = adapter.get_provider().app

        # More info on code vs access_token
        # http://stackoverflow.com/questions/8666316/facebook-oauth-2-0-code-and-token

        # Case 1: We received the access_token
        if attrs.get('access_token'):
            access_token = attrs.get('access_token')

        # Case 2: We received the authorization code
        elif attrs.get('code'):
            self.callback_url = getattr(view, 'callback_url', None)
            self.client_class = getattr(view, 'client_class', None)

            if not self.callback_url:
                raise serializers.ValidationError(
                    _("Define callback_url in view")
                )
            if not self.client_class:
                raise serializers.ValidationError(
                    _("Define client_class in view")
                )

            code = attrs.get('code')

            provider = adapter.get_provider()
            scope = provider.get_scope(request)
            client = self.client_class(
                request,
                app.client_id,
                app.secret,
                adapter.access_token_method,
                adapter.access_token_url,
                self.callback_url,
                scope
            )
            token = client.get_access_token(code)
            access_token = token['access_token']

        else:
            raise serializers.ValidationError(
                _("Incorrect input. access_token or code is required."))

        social_token = adapter.parse_token({'access_token': access_token})
        social_token.app = app

        try:
            login = self.get_social_login(adapter, app, social_token, access_token)
            complete_social_login(request, login)
        except Exception as e:
            print(e)
            raise serializers.ValidationError(_("User is already registered with this e-mail address."))

        if not login.is_existing:
            # We have an account already signed up in a different flow
            # with the same email address: raise an exception.
            # This needs to be handled in the frontend. We can not just
            # link up the accounts due to security constraints
            if allauth_settings.UNIQUE_EMAIL:
                # Do we have an account already with this email address?
                account_exists = get_user_model().objects.filter(
                    email=login.user.email,
                ).exists()
                if account_exists:
                    raise serializers.ValidationError(
                        _("User is already registered with this e-mail address.")
                    )

            login.lookup()
            login.save(request, connect=True)

        attrs['user'] = login.account.user

        return attrs

