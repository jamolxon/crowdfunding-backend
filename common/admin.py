from django.contrib import admin

from common.models import User
from common.models import CampaignViews


admin.site.register(User)


@admin.register(CampaignViews)
class CampaignViewsAdmin(admin.ModelAdmin):
    list_display = ("campaign", "user", "count")
