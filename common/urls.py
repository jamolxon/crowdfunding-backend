from django.urls import path

from common.views import UserProfileView, ProfileUpdateView

app_name = "common"

urlpatterns = [
    path("user/<int:pk>/", UserProfileView.as_view(), name="user-profile"),
    path("user/update/", ProfileUpdateView.as_view(), name="user-profile-update"),
]
