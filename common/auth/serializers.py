from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer as TokenObtainSerializer,
)
from rest_framework import serializers

from django.core.signing import BadSignature
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.password_validation import validate_password

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
