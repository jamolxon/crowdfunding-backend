from rest_framework import serializers

from common.models import User


class UserProfileSerializer(serializers.ModelSerializer):
    is_request_user = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "bio",
            "avatar_url",
            "is_request_user",
        )

    def get_is_request_user(self, obj):
        if (
            self.context["request"].user.is_authenticated
            and self.context["request"].user == obj
        ):
            return True
        return False


class ProfileUpdateSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    avatar = serializers.ImageField(required=False, write_only=True)
    bio = serializers.CharField(required=False)
    avatar_url = serializers.CharField(read_only=True)

    def update(self, instance, validated_data):
        avatar = validated_data.pop("avatar", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if avatar:
            instance.avatar = avatar

        instance.save()

        return instance
