from rest_framework import serializers

from campaign.models import (
    Campaign,
    CampaignCategory,
    CampaignTag,
    CampaignImage,
    Reward,
    Investment,
)


class CampaignTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampaignTag
        fields = ("id", "title")


class CampaignCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CampaignCategory
        fields = ("id", "title")


class CampaignImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampaignImage
        fields = ("id", "image_url")


class CampaignListSerializer(serializers.ModelSerializer):
    success_rate = serializers.SerializerMethodField()
    backers = serializers.SerializerMethodField()

    class Meta:
        model = Campaign
        fields = (
            "id",
            "title",
            "author",
            "image_url",
            "goal_amount",
            "current_amount",
            "duration",
            "success_rate",
            "backers",
        )

    def get_success_rate(self, obj):
        return 0

    def get_backers(self, obj):
        return 0


class CampaignDetailSerializer(serializers.ModelSerializer):
    success_rate = serializers.SerializerMethodField()
    backers = serializers.SerializerMethodField()
    tags = CampaignTagSerializer(many=True)
    campaign_images = CampaignImageSerializer(many=True)

    class Meta:
        model = Campaign
        fields = (
            "id",
            "title",
            "video_url",
            "image_url",
            "goal_amount",
            "current_amount",
            "duration",
            "success_rate",
            "backers",
            "content",
            "tags",
            "campaign_images",
        )

    def get_success_rate(self, obj):
        return 0

    def get_backers(self, obj):
        return 0


class RewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reward
        fields = ["id", "title", "amount"]


class CampaignSerializer(serializers.ModelSerializer):
    rewards = RewardSerializer(many=True, read_only=True)

    class Meta:
        model = Campaign
        fields = [
            "id",
            "title",
            "description",
            "goal_amount",
            "current_amount",
            "rewards",
        ]


class InvestmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investment
        fields = [
            "id",
            "user",
            "campaign",
            "reward",
            "amount",
            "status",
            "stripe_payment_intent_id",
            "created_at",
        ]
        read_only_fields = ["user", "status", "created_at"]


class CampaignCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = ("id", "title", "subtitle", "author", "category", "image", "video", "goal_amount", "start_date", "end_date", "content")

