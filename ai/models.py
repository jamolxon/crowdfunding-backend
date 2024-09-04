from django.db import models
from django.utils.translation import gettext_lazy as _


class CampaignData(models.Model):
    campaign_id = models.CharField(_("campaign id"), max_length=256)
    goal_amount = models.IntegerField(_("goal amount"))
    raised_amount = models.DecimalField(
        _("raised amount"), max_digits=19, decimal_places=10
    )
    duration_days = models.IntegerField(_("duration days"))
    number_of_backers = models.IntegerField(_("number of backers"))
    category = models.CharField(_("category"), max_length=256)
    currency = models.CharField(_("currency"), max_length=256)
    owner_experience = models.IntegerField(_("owner experience"))
    is_video_included = models.CharField(
        _("campaign video is included"), max_length=256
    )
    social_media_presence = models.IntegerField(_("social media presence"))
    number_of_updates = models.IntegerField(_("number of updates"))

    def __str__(self):
        return f"{self.campaign_id}"

    class Meta:
        db_table = "campaign_data"
        verbose_name = _("campaign data")
        verbose_name_plural = _("campaign data")


class Interaction(models.Model):
    user_id = models.CharField(_("user id"), max_length=256)
    campaign_id = models.CharField(_("campaign id"), max_length=256)
    interaction_type = models.CharField(_("interaction_type"), max_length=256)

    def __str__(self):
        return f"{self.user_id} - {self.campaign_id}"

    class Meta:
        db_table = "interaction"
        verbose_name = _("interaction")
        verbose_name_plural = _("interactions")
