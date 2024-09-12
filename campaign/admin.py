from django.contrib import admin

from campaign.models import (
    Campaign,
    CampaignTag,
    CampaignImage,
    CampaignCategory,
    Investment,
    Reward,
)


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "author",
        "start_date",
        "end_date",
        "goal_amount",
        "duration",
    )


@admin.register(CampaignTag)
class CampaignTagAdmin(admin.ModelAdmin):
    list_display = ("title",)


@admin.register(CampaignImage)
class CampaignImageAdmin(admin.ModelAdmin):
    list_display = ("campaign",)


@admin.register(CampaignCategory)
class CampaignCategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "parent")


@admin.register(Reward)
class RewardAdmin(admin.ModelAdmin):
    list_display = ("title", "amount")


@admin.register(Investment)
class InvestmentAdmin(admin.ModelAdmin):
    list_display = ("user", "campaign", "amount", "status")
