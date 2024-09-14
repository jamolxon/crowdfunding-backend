from django.db.models import F
from django.utils.deprecation import MiddlewareMixin

from common.hitcount.models import CampaignViews
from campaign.models import Campaign


VALID_PATHS = ["campaign", ]


class UserHandlerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")

        if request.user.is_authenticated and request.user.ip_address != ip:
            request.user.ip_address = ip
            request.user.device = request.META.get("HTTP_USER_AGENT")
            request.user.save()

        return response


class CampaignViewMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        try:
            if view_func.view_class.__name__ == "CampaignDetailView":
                # GET IP ADDRESS
                x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
                if x_forwarded_for:
                    ip = x_forwarded_for.split(",")[0]
                else:
                    ip = request.META.get("REMOTE_ADDR")

                campaign = Campaign.objects.get(id=view_kwargs["pk"])

                if request.user.is_authenticated:
                    if not CampaignViews.objects.filter(ip=ip, campaign=campaign).exists():
                        CampaignViews.objects.create(campaign=campaign, user=request.user, ip=ip)

                    CampaignViews.objects.filter(
                        campaign=campaign,
                        ip=ip,
                    ).update(count=F("count") + 1, user=request.user)

                else:
                    if not CampaignViews.objects.filter(
                        ip=ip,
                        campaign=campaign
                    ).exists():
                        CampaignViews.objects.create(campaign=campaign, ip=ip)

                    CampaignViews.objects.filter(
                        campaign=campaign,
                        ip=ip,
                    ).update(count=F("count") + 1)

        except Exception as e:  # noqa: E722
            print(e)
