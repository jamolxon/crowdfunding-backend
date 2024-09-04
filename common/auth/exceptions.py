from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import APIException


class UserLoggedIn(APIException):
    status_code = 400
    default_detail = _("Siz allaqachon tizimga kirgansiz")
    default_code = "user_logged_in"
