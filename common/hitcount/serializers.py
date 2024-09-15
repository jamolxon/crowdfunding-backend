from rest_framework import serializers

from common.models import CampaignViews


class CampaignViewsSerializer(serializers.ModelSerializer):
    campaign = serializers.StringRelatedField()
    user = serializers.StringRelatedField()

    class Meta:
        model = CampaignViews
        fields = ("id", "campaign", "user", "count")
