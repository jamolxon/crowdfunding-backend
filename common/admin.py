from django.contrib import admin

from common.models import User
from common.models import CampaignViews


admin.site.register(User)

admin.site.register(CampaignViews)
