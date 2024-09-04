import os
import csv

from django.db import IntegrityError, transaction

from ai.models import CampaignData, Interaction
from core.settings import BASE_DIR


def load_campaign_data():

    with open(
        os.path.join(BASE_DIR, "ai/datasets/campaign_data.csv"),
    ) as csv_file:
        reader = csv.DictReader(csv_file)
        id_count = 1
        for info in reader:
            try:
                with transaction.atomic():
                    CampaignData.objects.create(
                        id=id_count,
                        campaign_id=info["CampaignID"],
                        goal_amount=info["GoalAmount"],
                        raised_amount=info["RaisedAmount"],
                        duration_days=info["DurationDays"],
                        number_of_backers=info["NumBackers"],
                        category=info["Category"],
                        currency=info["Currency"],
                        owner_experience=info["OwnerExperience"],
                        is_video_included=info["VideoIncluded"],
                        social_media_presence=info["SocialMediaPresence"],
                        number_of_updates=info["NumUpdates"],
                    )
            except IntegrityError:
                campaign = CampaignData.objects.get(id=id_count)
                campaign.campaign_id = info["CampaignID"]
                campaign.goal_amount = info["GoalAmount"]
                campaign.raised_amount = info["RaisedAmount"]
                campaign.duration_days = info["DurationDays"]
                campaign.number_of_backers = info["NumBackers"]
                campaign.category = info["Category"]
                campaign.currency = info["Currency"]
                campaign.owner_experience = info["OwnerExperience"]
                campaign.is_video_included = info["VideoIncluded"]
                campaign.social_media_presence = info["SocialMediaPresence"]
                campaign.number_of_updates = info["NumUpdates"]
                campaign.save()

            id_count += 1

        return CampaignData.objects.all()


def load_interaction_data():

    with open(
        os.path.join(BASE_DIR, "ai/datasets/interactions.csv"),
    ) as csv_file:
        reader = csv.DictReader(csv_file)
        id_count = 1
        for info in reader:
            try:
                with transaction.atomic():
                    Interaction.objects.create(
                        id=id_count,
                        user_id=info["UserID"],
                        campaign_id=info["CampaignID"],
                        interaction_type=info["InteractionType"],
                    )
            except IntegrityError:
                interaction = Interaction.objects.get(id=id_count)
                interaction.user_id = info["UserID"]
                interaction.campaign_id = info["CampaignID"]
                interaction.interaction_type = info["InteractionType"]
                interaction.save()

            id_count += 1

        return Interaction.objects.all()
