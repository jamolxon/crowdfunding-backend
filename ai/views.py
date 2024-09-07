import getpass
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse, HttpResponse
from .models import *
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import ChatMessage
from .serializers import ChatMessageSerializer
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv



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

# AI - Chatbot
load_dotenv()


def chatbot_base(request):
    return JsonResponse({
        "message": "Welcome to the InvestMe ChatBot API. Use /respond/ to interact with the chatbot or /history/ to view chat history."
    })


system_prompt = (
"""
    Never answer questions that are not related to crowdfunding.
    You are an AI-powered assistant for InvestMe, a crowdfunding platform that helps entrepreneurs and creators bring their ideas to life.
    Your role is to guide users through the platform, helping them understand how to create, manage, and support crowdfunding campaigns.
    You provide detailed explanations on the process of launching a campaign, setting funding goals, and engaging with backers.
    You also offer insights on best practices for marketing and promoting campaigns to maximize success.

    Additionally, you assist users with any technical issues they might encounter, provide customer support, and answer frequently asked questions
    related to crowdfunding. You are knowledgeable, friendly, and committed to ensuring that every user has a smooth and successful experience
    on InvestMe. Always prioritize clarity and helpfulness in your responses, and ensure that users feel supported and informed.
"""
)


@api_view(['POST'])
def chatbot_respond(request):
    user_message = request.data.get('message')
    chat_history = ChatMessage.objects.all()

    # Generate the chat history string
    history_str = ""
    for message in chat_history:
        role = "human" if message.role == "human" else "ai"
        history_str += f"{role}: {message.content}\n"

    # Define the prompt template
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            (f"Chat history: {history_str}"),
            ("human", "{query}")
        ]
    )

    # Initialize the LLM with the specified model and temperature
    llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0.7)

    # Create the chain with the prompt and LLM
    chain = prompt | llm | StrOutputParser()

    # Get the response generator
    response_generator = chain.stream({
        "chat_history": history_str,
        "query": user_message
    })

    # Concatenate the generator output to form the full response
    response = ''.join([part for part in response_generator])

    # Save the human message and AI response
    human_message = ChatMessage.objects.create(role="human", content=user_message)
    ai_message = ChatMessage.objects.create(role="ai", content=response)

    # Serialize the response
    ai_message_serialized = ChatMessageSerializer(ai_message)

    return Response(ai_message_serialized.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_chat_history(request):
    messages = ChatMessage.objects.all()
    serializer = ChatMessageSerializer(messages, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
def delete_chat_history(request):
    # Delete all chat messages
    ChatMessage.objects.all().delete()
    return Response({"status": "Chat history deleted."}, status=status.HTTP_200_OK)