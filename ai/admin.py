from django.contrib import admin

from ai.models import CampaignData, Interaction


admin.site.register(CampaignData)


@admin.register(Interaction)
class InteractionAdmin(admin.ModelAdmin):
    list_display = ("user_id", "campaign_id", "interaction_type")
    list_filter = ("interaction_type",)
