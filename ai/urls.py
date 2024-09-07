from django.urls import path
from . import views

urlpatterns = [
    path('campaign/predict/<str:campaign_id>/', views.campaign_predict, name='campaign_predict'),
    path('recommend/<str:user_id>/', views.recommend_campaigns, name='recommend_campaigns'),
    path('chatbot/', views.chatbot_base, name='chatbot_base'),
    path('chatbot/respond/', views.chatbot_respond, name='chatbot_respond'),
    path('chatbot/history/', views.get_chat_history, name='get_chat_history'),
    path('chatbot/history/delete/', views.delete_chat_history, name='delete_chat_history')
]