from rest_framework.serializers import ModelSerializer
from PlaystoreIngestion.models import PlaystoreFeedback
from FeedbackIngestion.models import Feedback, FeedbackMetadata


class PlaystoreFeedbackSerializer(ModelSerializer):
    class Meta:
        model = PlaystoreFeedback
        fields = [
            "application", "app_version", "review_id",
            "parent_review_id", "username", "title", "description",
            "ratings", "created_at_playstore", "updated_at_playstore"
        ]

    def populate_fields(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        return instance

    def save(self, **kwargs):

        assert hasattr(self, '_errors'), (
            'You must call `.is_valid()` before calling `.save()`.'
        )

        assert not self.errors, (
            'You cannot call `.save()` on a serializer with invalid data.'
        )

        validated_data = {**self.validated_data, **kwargs}

        playstore_feedback = PlaystoreFeedback()
        self.populate_fields(playstore_feedback, validated_data)
        feedback = None
        feedback_metadata = None
        try:
            feedback = Feedback.objects.get(feedback_id=playstore_feedback.get_review_id(playstore_feedback.review_id))
            feedback_metadata = FeedbackMetadata.objects.get(feedback_id=feedback.feedback_id)
        except Feedback.DoesNotExist:
            pass

        if feedback:
            playstore_feedback.update(feedback, feedback_metadata)
        else:
            playstore_feedback.save()

        return playstore_feedback
