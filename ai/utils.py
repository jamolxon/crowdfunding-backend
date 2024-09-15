import os
import csv
from django.db import IntegrityError, transaction
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage as storage
from ai.models import CampaignData, Interaction
from campaign.models import *
from core.settings import BASE_DIR
from PIL import Image, ImageDraw, ImageFont
import io

# IMAGE GENERATION

def image_generator(title, id):
    image = Image.new('RGB', (1200, 800), color=(0, 255, 0))
    draw = ImageDraw.Draw(image)

    try:
        font = ImageFont.truetype("arial.ttf", 50)
    except IOError:
        font = ImageFont.load_default()

    # Calculate text size and position
    bbox = draw.textbbox((0, 0), title, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    position = ((1200 - text_width) // 2, (800 - text_height) // 2)

    # Add the text to the image
    draw.text(position, title, font=font, fill=(255, 255, 255))

    # Save the image to an in-memory file
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    
    # Return the in-memory image as ContentFile
    return ContentFile(img_byte_arr.getvalue(), name=f'{title}_{id}.png')



## LOADING ALL DATA

def load_campaign_data():

    with open(
        os.path.join(BASE_DIR, "ai/datasets/mock_campaigns_data.csv"),
    ) as csv_file:
        reader = csv.DictReader(csv_file)
        id_count = 1
        for info in reader:
            try:
                with transaction.atomic():
                    image = image_generator(info["Title"], id_count)
                    user, created = User.objects.get_or_create(
                        first_name=info["Author"].split()[0],
                        last_name=info["Author"].split()[1] if len(info["Author"].split()) > 1 else '',
                    )

                    category, created = CampaignCategory.objects.get_or_create(
                        title=info["Category"]
                    )
                    
                    tags = info["Tags"].strip('][').split(', ')

                    bulk_list = list()
                    for tag in tags:
                        bulk_list.append(CampaignTag(title=f"{tag}"))
                    
                    tags = CampaignTag.objects.bulk_create(bulk_list)

                    campaign = Campaign.objects.create(
                        title = info["Title"],
                        subtitle = info["Subtitles"],
                        author = user,
                        category = category,
                        goal_amount = info["Goal Amount"],
                        current_amount = info["Current Amount"],
                        is_top = info["Is_Top"],
                        is_recommended = info["Is Recommended"],
                        start_date = info["Start Date"],
                        end_date = info["End Date"],
                        creation_date = info["Creation Date"],
                        content = info["Content"],
                    )
                    for tag in tags:
                        campaign.tags.add(tag)

                    campaign.image.save(f'{info["Title"]}_{id_count}.png', image, save=True)
                    campaign.save()

                        
                
            except IntegrityError:
                campaign = Campaign.objects.get(id=id_count)
                campaign.title = info["Title"]
                campaign.subtitle = info["Subtitles"]
                campaign.author = info["Author"]
                campaign.category = info["Category"]
                campaign.goal_amount = info["Goal Amount"]
                campaign.current_amount = info["Current Amount"]
                campaign.image = image_generator(info["Title"], id_count),
                campaign.is_top = info["Is_Top"]
                campaign.is_recommended = info['Is Recommended']
                campaign.start_date = info["Start Date"]
                campaign.end_date = info["End Date"]
                campaign.creation_date = info["Creation Date"]
                campaign.content = info["Content"]
                campaign.tags = info["Tags"]
                campaign.save()

            id_count += 1

        return Campaign.objects.all()
    

def load_users_data():
    with open(
        os.path.join(BASE_DIR, "ai/datasets/mock_users_data.csv"),
    ) as csv_file:
        reader = csv.DictReader(csv_file)
        id_count = 1
        for info in reader:
            try:
                with transaction.atomic():
                    User.objects.create(
                        first_name = info["First Name"],
                        last_name = info["Last Name"],
                        email = info["Email"],
                        bio= info["Bio"],
                        password = info["Password"],
                        role = info["Role"]
                        
                    )
                        
                
            except IntegrityError:
                user = User.objects.get(id=id_count)
                user.first_name = info["First Name"],
                user.last_name = info["Last Name"],
                user.email = info["Email"],
                user.bio= info["Bio"],
                user.password = info["Password"],
                user.role = info["Role"]
                user.save()

            id_count += 1

        return User.objects.all()


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
