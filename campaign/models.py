from datetime import timedelta

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.core.validators import FileExtensionValidator

from django_resized import ResizedImageField

from helpers.models import BaseModel
from common.models import User


class InvestmentChoices(models.TextChoices):
    pending = "pending", _("Pending")
    approved = "approved", _("Approved")
    returned = "returned", _("Returned")


class CampaignCategory(BaseModel):
    title = models.CharField(_("title"), max_length=256)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="children",
        verbose_name=_("parent"),
    )

    def __str__(self):
        return f"{self.title}"

    class Meta:
        db_table = "campaign_category"
        verbose_name = _("campaign category")
        verbose_name_plural = _("campaign categories")


class CampaignTag(BaseModel):
    title = models.CharField(_("title"), max_length=256)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        db_table = "campaign_tag"
        verbose_name = _("campaign tag")
        verbose_name_plural = _("campaign tags")


class Campaign(BaseModel):
    title = models.CharField(_("title"), max_length=256)
    subtitle = models.CharField(_("subtitle"), max_length=256)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="campaigns",
        verbose_name=_("author"),
    )
    category = models.ForeignKey(
        CampaignCategory,
        on_delete=models.CASCADE,
        related_name="campaigns",
        verbose_name=_("category"),
        null=True,
    )
    goal_amount = models.DecimalField(max_digits=10, decimal_places=2)
    current_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    image = ResizedImageField(
        size=[1200, 800],
        crop=["middle", "center"],
        verbose_name=_("image"),
        quality=90,
        upload_to="campaigns/%Y/%m",
    )
    video = models.FileField(
        _("video"),
        upload_to="campaigns/videos/%Y/%m",
        validators=[
            FileExtensionValidator(["mov", "mpeg", "avi", "3gp", "wmv", "flv", "mp4"])
        ],
        null=True,
    )
    is_top = models.BooleanField(_("campaign is top"), default=False)
    is_recommended = models.BooleanField(_("campaign is recommended"), default=False)
    start_date = models.DateTimeField(_("start date"), default=timezone.now)
    end_date = models.DateTimeField(
        _("end date "), default=timezone.now() + timedelta(days=21)
    )
    creation_date = models.DateTimeField(default=timezone.now)
    content = models.TextField()
    tags = models.ManyToManyField(
        CampaignTag, related_name="campaigns", verbose_name=_("tags")
    )

    @property
    def image_url(self):
        return f"{settings.HOST}{self.image.url}" if self.image else ""

    @property
    def video_url(self):
        return f"{settings.HOST}{self.video.url}" if self.video else ""

    @property
    def duration(self):
        if (self.end_date - timezone.now()).days > 0:
            return (self.end_date - timezone.now()).days
        return 0

    def __str__(self):
        return f"{self.title}"

    class Meta:
        db_table = "campaign"
        verbose_name = _("campaign")
        verbose_name_plural = _("campaigns")


class CampaignImage(BaseModel):
    image = ResizedImageField(
        size=[1200, 800],
        crop=["middle", "center"],
        verbose_name=_("image"),
        quality=90,
        upload_to="campaigns/images/%Y/%m",
    )
    campaign = models.ForeignKey(
        Campaign,
        on_delete=models.CASCADE,
        related_name="campaign_images",
        verbose_name=_("campaign"),
    )

    @property
    def image_url(self):
        return f"{settings.HOST}{self.image.url}" if self.image else ""

    def __str__(self):
        return f"{self.campaign}"

    class Meta:
        db_table = "campaign_image"
        verbose_name = _("campaign image")
        verbose_name_plural = _("campaign images")


class Reward(BaseModel):
    title = models.CharField(_("title"), max_length=256)
    description = models.TextField(_("description"), max_length=256)
    amount = models.DecimalField(_("amount"), max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        db_table = "reward"
        verbose_name = _("reward")
        verbose_name_plural = _("rewards")


class Investment(BaseModel):
    user = models.ForeignKey(
        User,
        related_name="investments",
        on_delete=models.CASCADE,
        verbose_name=_("user"),
    )
    campaign = models.ForeignKey(
        Campaign,
        related_name="investments",
        on_delete=models.CASCADE,
        verbose_name=_("campaign"),
    )
    reward = models.ForeignKey(
        Reward,
        related_name="investments",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name=_("reward"),
    )
    amount = models.DecimalField(_("amount"), max_digits=10, decimal_places=2)
    status = models.CharField(
        _("status"),
        max_length=16,
        choices=InvestmentChoices.choices,
        default=InvestmentChoices.pending,
    )
    stripe_payment_intent_id = models.CharField(
        _("stripe payment intent id"), max_length=255, unique=True
    )

    def __str__(self):
        return f"{self.user} invested {self.amount} in {self.campaign} - {self.status}"

    class Meta:
        db_table = "investment"
        verbose_name = _("investment")
        verbose_name_plural = _("investments")
