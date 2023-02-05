from rest_framework.serializers import ModelSerializer
from DiscourseIngestion.models import DiscourseFeedback
from FeedbackIngestion.models import Feedback, FeedbackMetadata


class DiscourseFeedbackSerializer(ModelSerializer):

    class Meta:
        model = DiscourseFeedback
        fields = [
            "application", "post_id", "username", "title", "description",
            "parent_post_id", "like_count", "created_at_discourse",
            "updated_at_discourse",
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

        discourse_feedback = DiscourseFeedback()
        self.populate_fields(discourse_feedback, validated_data)
        feedback = None
        feedback_metadata = None
        try:
            feedback = Feedback.objects.get(feedback_id=discourse_feedback.get_post_id(discourse_feedback.post_id))
            feedback_metadata = FeedbackMetadata.objects.get(feedback_id=feedback.feedback_id)
        except Feedback.DoesNotExist:
            pass

        if feedback:
            discourse_feedback.update(feedback, feedback_metadata)
        else:
            discourse_feedback.save()

        return discourse_feedback

