from django.urls import path

from campaign.views import (
    CampaignCategoryListView,
    CampaignTopListView,
    CampaignRecommendedListView,
    CampaignDetailView,
    StatisticsAPIView,
    CampaignCategoryChildrenListView,
    CampaignListView,
)


urlpatterns = [
    path("", CampaignListView.as_view(), name="campaign-list"),
    path("category/", CampaignCategoryListView.as_view(), name="campaign-category"),
    path(
        "category/<int:pk>/",
        CampaignCategoryChildrenListView.as_view(),
        name="campaign-subcategory",
    ),
    path("top/", CampaignTopListView.as_view(), name="campaign-top"),
    path(
        "recommended/",
        CampaignRecommendedListView.as_view(),
        name="campaign-recommended",
    ),
    path("statictics/", StatisticsAPIView.as_view(), name="campaign-statistics"),
    path("<int:pk>/", CampaignDetailView.as_view(), name="campaign-detail"),
]
