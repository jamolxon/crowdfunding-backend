from django.urls import path

from common.views import UserProfileView, ProfileUpdateView
from common.hitcount.views import CampaignViewsListView

app_name = "common"

urlpatterns = [
    path("user/<int:pk>/", UserProfileView.as_view(), name="user-profile"),
    path("user/update/", ProfileUpdateView.as_view(), name="user-profile-update"),
    path("user/views/", CampaignViewsListView.as_view(), name="user-campaign-views"),
]
