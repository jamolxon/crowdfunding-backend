from django.urls import path
from . import views

urlpatterns = [
    path('campaign/predict/<str:campaign_id>/', views.campaign_predict, name='campaign_predict'),
    path('recommend/<str:user_id>/', views.recommend_campaigns, name='recommend_campaigns'),
]