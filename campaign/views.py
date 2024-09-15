# import stripe

from django.db.models import Q, F, Count

# from django.conf import settings
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser
from rest_framework.generics import (
    ListAPIView,
    UpdateAPIView,
    RetrieveAPIView,
    GenericAPIView,
    CreateAPIView,
)
from rest_framework.views import APIView
from rest_framework.response import Response

from campaign.serializers import (
    CampaignCategorySerializer,
    CampaignListSerializer,
    CampaignDetailSerializer,
    InvestmentSerializer,
    CampaignCreateSerializer
)
from campaign.models import Campaign, CampaignCategory, Investment, Reward
from helpers import pagination

# stripe.api_key = settings.STRIPE_TEST_SECRET_KEY


class CampaignCategoryListView(ListAPIView):
    queryset = CampaignCategory.objects.filter(parent__isnull=True)
    serializer_class = CampaignCategorySerializer
    pagination_class = None


class CampaignCategoryChildrenListView(ListAPIView):
    queryset = CampaignCategory.objects.all()
    serializer_class = CampaignCategorySerializer
    lookup_field = "pk"
    pagination_class = None

    def filter_queryset(self, queryset):
        return queryset.filter(parent_id=self.kwargs["pk"])


class CampaignTopListView(ListAPIView):
    queryset = Campaign.objects.filter(is_top=True).order_by("-creation_date")[:8]
    serializer_class = CampaignListSerializer
    pagination_class = None


class CampaignRecommendedListView(ListAPIView):
    queryset = Campaign.objects.filter(is_recommended=True).order_by("-creation_date")[
        :8
    ]
    serializer_class = CampaignListSerializer
    pagination_class = None


class CampaignListView(ListAPIView):
    """
    for search, use: ?search=
    """

    queryset = Campaign.objects.all()
    serializer_class = CampaignListSerializer
    pagination_class = pagination.PageSix

    def filter_queryset(self, queryset):
        search = self.request.GET.get("search", None)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search)
                | Q(subtitle__icontains=search)
                | Q(category__title__icontains=search)
                | Q(category__parent__title__icontains=search)
            )

        return queryset


class CampaignDetailView(RetrieveAPIView):
    queryset = Campaign.objects.all().annotate(unique_views=Count("views"))
    serializer_class = CampaignDetailSerializer
    lookup_field = "pk"

    def retrieve(self, request, *args, **kwargs):
        Campaign.objects.filter(id=self.kwargs["pk"]).update(view_count=F("view_count") + 1)
        return super().retrieve(request, *args, **kwargs)


class StatisticsAPIView(APIView):
    def get(self, request):
        return Response(
            {"campigns": Campaign.objects.all().count(), "investors": 0, "raised": 0}
        )



class CampaignCreateView(CreateAPIView):
    queryset = Campaign.objects.all()
    serializer_class = CampaignCreateSerializer
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser, )


class CampaignUpdateView(UpdateAPIView):
    queryset = Campaign.objects.all()
    serializer_class = CampaignCreateSerializer
    permission_classes = (IsAuthenticated,)


class CreatePaymentIntentView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    # def post(self, request, *args, **kwargs):
    #     amount = request.data.get('amount')

    #     try:
    #         intent = stripe.PaymentIntent.create(
    #             amount=int(float(amount) * 100),  # Stripe uses cents
    #             currency='usd',
    #             payment_method_types=['card'],
    #             description='Investment Payment'
    #         )
    #         return Response({'client_secret': intent.client_secret}, status=status.HTTP_200_OK)
    #     except stripe.error.StripeError as e:
    #         return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class InvestmentCreateView(CreateAPIView):
    serializer_class = InvestmentSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data
        campaign_id = data.get("campaign_id")
        reward_id = data.get("reward_id")
        amount = data.get("amount")
        stripe_payment_intent_id = data.get("stripe_payment_intent_id")

        try:
            campaign = Campaign.objects.get(id=campaign_id)
            reward = Reward.objects.get(id=reward_id)
        except (Campaign.DoesNotExist, Reward.DoesNotExist):
            return Response(
                {"detail": "Invalid campaign or reward."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if amount != reward.amount:
            return Response(
                {"detail": "Amount does not match the reward amount."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        investment = Investment.objects.create(
            user=request.user,
            campaign=campaign,
            reward=reward,
            amount=amount,
            stripe_payment_intent_id=stripe_payment_intent_id,
        )

        campaign.current_amount += amount
        campaign.save()

        return Response(
            InvestmentSerializer(investment).data, status=status.HTTP_201_CREATED
        )


