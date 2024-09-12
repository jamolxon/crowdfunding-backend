from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.signing import TimestampSigner

from django_resized import ResizedImageField

from common.manager import UserManager


class RoleChoices(models.TextChoices):
    user = "user", _("User")
    staff = "staff", _("Moderator")
    superuser = "superuser", _("Superuser")


class User(AbstractUser):
    INVALID_CODE = "######"
    username = None

    first_name = models.CharField(_("first name"), max_length=256)
    last_name = models.CharField(_("last name"), max_length=256)
    email = models.EmailField(
        _("email"),
        unique=True,
        error_messages={
            "error": _("Email exists!"),
        },
        null=True,
    )
    bio = models.TextField(_("bio"), blank=True)
    avatar = ResizedImageField(
        size=[500, 500],
        crop=["middle", "center"],
        verbose_name=_("avatar"),
        quality=90,
        upload_to="user/%Y/%m",
        null=True,
    )
    role = models.CharField(
        _("user role"),
        max_length=12,
        choices=RoleChoices.choices,
        default=RoleChoices.user,
    )

    code = models.CharField(_("code"), max_length=8, blank=True, null=True)
    code_expiration = models.DateTimeField(_("code expiration"), default=timezone.now)

    created_at = models.DateTimeField(_("date created"), auto_now_add=True, null=True)
    updated_at = models.DateTimeField(_("date updated"), auto_now=True)

    # SETTINGS
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    signer = TimestampSigner(sep=":")

    objects = UserManager()

    @property
    def avatar_url(self):
        return f"{settings.HOST}{self.avatar.url}" if self.avatar else ""

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = None

        super().save(*args, **kwargs)

    class Meta:
        db_table = "user"
        swappable = "AUTH_USER_MODEL"
        verbose_name = _("user")
        verbose_name_plural = _("users")
