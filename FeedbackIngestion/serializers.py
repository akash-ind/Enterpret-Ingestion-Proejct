from rest_framework.serializers import ModelSerializer
from FeedbackIngestion.models import Feedback, FeedbackMetadata

class FeedbackSerializers(ModelSerializer):
    class Meta:
        model = Feedback
        fields = ["application", "feedback_id", "parent_feedback", "title", "description", "impact"]

