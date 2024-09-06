from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse, HttpResponse
from .models import *


@api_view(['GET'])
def campaign_predict(request, campaign_id):
    try:
        
        campaign = CampaignData.objects.get(campaign_id=campaign_id)

        input_data = {
            'CampaignID': campaign_id,
            'GoalAmount': campaign.goal_amount,
            'RaisedAmount': campaign.raised_amount,
            'DurationDays': campaign.duration_days,
            'NumBackers': campaign.number_of_backers,
            'Category': campaign.category,
            'Currency': campaign.currency,
            'OwnerExperience': campaign.owner_experience,
            'VideoIncluded': campaign.is_video_included,
            'SocialMediaPresence': campaign.social_media_presence,
            'NumUpdates': campaign.number_of_updates,
        }

        campaign_analyzer = CampaignAnalysis()
        result = campaign_analyzer.predict(input_data)

        if isinstance(result, float):  
            return JsonResponse({'CampaignID': campaign_id, 'SuccessRate': f'{result:.2f}%'})
        else:  # Prediction (e.g., 0 or 1 for success/failure)
            return JsonResponse({'CampaignID': campaign_id, 'Prediction': int(result)})
    
    except CampaignData.DoesNotExist:
        return HttpResponse(status=404, content=f'CampaignID {campaign_id} not found')
    except Exception as e:
        return HttpResponse(status=500, content=f'Error: {str(e)}')


@api_view(['GET'])
def recommend_campaigns(request, user_id, top_n=5):
    try:
        interactions = Interaction.objects.filter(user_id=user_id)

        if not interactions.exists():
            # Fallback: recommend the top N popular campaigns (based on the number of backers)
            popular_campaigns = CampaignData.objects.order_by('-number_of_backers')[:top_n]
            recommended_campaigns = [campaign.campaign_id for campaign in popular_campaigns]

            return Response({
                'UserID': user_id, 
                'Recommendations': recommended_campaigns,
                'Message': 'No interaction data found. Recommending popular campaigns instead.'
            })
        
        input_data = {
            'UserID': [interaction.user_id for interaction in interactions],
            'CampaignID': [interaction.campaign_id for interaction in interactions],
            'InteractionType': [interaction.interaction_type for interaction in interactions],
        }

        recommender = RecommendationSystem()

        recommendations = recommender.recommend(input_data=input_data, user_id=user_id, top_n=top_n)

        return Response({'UserID': user_id, 'Recommendations': recommendations})

    except Exception as e:
        return Response({'error': str(e)}, status=500)
