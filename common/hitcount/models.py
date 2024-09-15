from django.db import models
from django.utils.translation import gettext_lazy as _

from helpers.models import BaseModel


class CampaignViews(BaseModel):
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)
    user = models.OneToOneField("common.User", on_delete=models.CASCADE, related_name="views", null=True)
    campaign = models.ForeignKey(
        "campaign.Campaign", on_delete=models.SET_NULL, null=True, related_name="views"
    )
    ip = models.CharField(max_length=40)
    count = models.BigIntegerField(default=0)

    class Meta:
        ordering = ("-created", "-modified")
        get_latest_by = "created"
        verbose_name = _("campaign views")
        verbose_name_plural = _("campaign views")

    def __str__(self):
        return f"{self.campaign.title}"

