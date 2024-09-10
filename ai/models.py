from django.db import models
from django.utils.translation import gettext_lazy as _
import joblib
from sklearn.preprocessing import LabelEncoder
from sklearn.decomposition import TruncatedSVD
import pandas as pd
import os
from django.conf import settings


# Datasets

class CampaignData(models.Model):
    campaign_id = models.CharField(_("campaign id"), max_length=256)
    goal_amount = models.IntegerField(_("goal amount"))
    raised_amount = models.DecimalField(
        _("raised amount"), max_digits=19, decimal_places=10
    )
    duration_days = models.IntegerField(_("duration days"))
    number_of_backers = models.IntegerField(_("number of backers"))
    category = models.CharField(_("category"), max_length=256)
    currency = models.CharField(_("currency"), max_length=256)
    owner_experience = models.IntegerField(_("owner experience"))
    is_video_included = models.CharField(
        _("campaign video is included"), max_length=256
    )
    number_of_updates = models.IntegerField(_("number of updates"))
    user_id = models.CharField(_("user id"), max_length=256, default='default_user')

    def __str__(self):
        return f"{self.campaign_id}"

    class Meta:
        db_table = "campaign_data"
        verbose_name = _("campaign data")
        verbose_name_plural = _("campaign data")


class Interaction(models.Model):
    user_id = models.CharField(_("user id"), max_length=256)
    campaign_id = models.CharField(_("campaign id"), max_length=256)
    interaction_type = models.CharField(_("interaction_type"), max_length=256)

    def __str__(self):
        return f"{self.user_id} - {self.campaign_id}"

    class Meta:
        db_table = "interaction"
        verbose_name = _("interaction")
        verbose_name_plural = _("interactions")



# ML Models 
    
## Campaign Analysis
class CampaignAnalysis:
    def __init__(self):

        self.model = os.path.join(settings.BASE_DIR, 'ai', 'models', 'campaign_success_analysis_random_forest.pkl')
        self.label_encoders = os.path.join(settings.BASE_DIR, 'ai', 'models', 'label_encoders.pkl')
        
        # Loading Decision Tree Classifier

        if os.path.exists(self.model):
            print(f"Loading model from: {self.model}")
            try:
                self.model = joblib.load(self.model)
                print(f"Model loaded successfully. Model type: {type(self.model)}")
            except Exception as e:
                raise ValueError(f"Error loading the model: {e}")
        else:
            raise FileNotFoundError(f"Model file not found at {self.model}")
        
        # Loading Label Encoders 

        if os.path.exists(self.label_encoders):
            print(f"Loading label encoders from: {self.label_encoders}")
            try:
                self.label_encoders = joblib.load(self.label_encoders)
                print("Label encoders loaded successfully.")
            except Exception as e:
                raise ValueError(f"Error loading the label encoders: {e}")
        else:
            raise FileNotFoundError(f"Label encoders file not found at {self.label_encoders}")

    def predict(self, input_data):
        preprocessed_data = self.preprocess(input_data)

        
        if hasattr(self.model, 'predict_proba'):
            probabilities = self.model.predict_proba(preprocessed_data)
            success_probability = probabilities[0][1]  # Assuming class 1 is "success"
            success_rate = success_probability * 100
            return success_rate
        
        elif hasattr(self.model, 'predict'):
            prediction = self.model.predict(preprocessed_data)
            return prediction  # Return prediction if model does not provide probabilities
        else:
            raise AttributeError("Model does not support 'predict' or 'predict_proba' methods")

    
    def preprocess(self, input_data):
        df = pd.DataFrame([input_data])

        for column in df.columns:
            if column in self.label_encoders:  # Ensure encoder exists for the column
                try:
                    df[column] = self.label_encoders[column].transform(df[column])
                except Exception as e:
                    raise ValueError(f"Error encoding column '{column}': {e}")
            else:
                print(f"No label encoder found for column '{column}', skipping encoding.")
        
        return df


## Recommendation System
class RecommendationSystem:
    def __init__(self, n_components=1):
        self.svd = TruncatedSVD(n_components=n_components, random_state=42)

    def preprocess(self, input_data):
        df = pd.DataFrame(input_data)

        matrix = df.pivot_table(index='UserID', columns='CampaignID', values='InteractionType', aggfunc='count', fill_value=0)

        return matrix

    def recommend(self, input_data, user_id, top_n=5):
        matrix = self.preprocess(input_data=input_data)

        if user_id not in matrix.index:
            raise ValueError(f"User {user_id} not found in interaction data.")

        recommended_campaigns = self.recommender(matrix, user_id, top_n=top_n)

        return recommended_campaigns

    def recommender(self, matrix, user_id, top_n=5):

        user_factors = self.svd.fit_transform(matrix) 
        campaign_factors = self.svd.components_.T       

        user_index = matrix.index.get_loc(user_id)

        user_ratings = user_factors[user_index, :].dot(campaign_factors.T)

        top_campaigns = user_ratings.argsort()[::-1][:top_n]

        recommended_campaigns = matrix.columns[top_campaigns]

        return list(recommended_campaigns)
    

# AI-ChatBot 
class ChatMessage(models.Model):
    role = models.CharField(max_length=10) # Human or AI
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.role}: {self.content[:50]}"