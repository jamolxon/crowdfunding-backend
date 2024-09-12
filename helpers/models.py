from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models import FileField
from django.forms import forms
from django.template.defaultfilters import filesizeformat

from helpers.utils import get_current_user


class BaseModel(models.Model):
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="%(class)s_createdby",
        editable=False,
    )
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="%(class)s_modifiedby",
        null=True,
        blank=True,
        editable=False,
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        user = get_current_user()
        if user and user.is_authenticated():
            self.modified_by = user
            if not self.id:
                self.created_by = user

        super().save(*args, **kwargs)


class ValidatedFileField(FileField):
    """
    Same as FileField, but you can specify:
        * content_types - list containing allowed content_types. Example: ['application/pdf', 'image/jpeg']
        * max_upload_size - a number indicating the maximum file size allowed for upload.
            2.5MB - 2621440
            5MB - 5242880
            10MB - 10485760
            20MB - 20971520
            50MB - 5242880
            100MB 104857600
            250MB - 214958080
            500MB - 429916160"""

    def __init__(self, *args, **kwargs):
        self.content_types = kwargs.pop("content_types")
        self.max_upload_size = kwargs.pop("max_upload_size")

        super(ValidatedFileField, self).__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        data = super(ValidatedFileField, self).clean(*args, **kwargs)

        file = data.file
        try:
            content_type = file.content_type
            if content_type in self.content_types:
                if file._size > self.max_upload_size:
                    raise forms.ValidationError(
                        _("Please keep filesize under %s. Current filesize %s")
                        % (
                            filesizeformat(self.max_upload_size),
                            filesizeformat(file._size),
                        )
                    )
            else:
                raise forms.ValidationError(_("Filetype not supported."))
        except AttributeError:
            pass

        return data
