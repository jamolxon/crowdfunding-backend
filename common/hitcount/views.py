from rest_framework.generics import ListAPIView

from common.hitcount.serializers import CampaignViewsSerializer
from common.models import CampaignViews


class CampaignViewsListView(ListAPIView):
    queryset = CampaignViews.objects.all().order_by("-id")
    serializer_class = CampaignViewsSerializer
    pagination_class = None
