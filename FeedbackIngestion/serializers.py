from rest_framework.serializers import ModelSerializer
from FeedbackIngestion.models import DiscourseFeedback, Feedback, FeedbackMetadata


class DiscourseFeedbackSerializer(ModelSerializer):
    class Meta:
        model = DiscourseFeedback
        fields = "__all__"
        abstract = True

    def populate_fields(self, instance, validated_data):
        # Todo: Support Many to many fields:
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        return instance

    def save(self, **kwargs):

        assert hasattr(self, '_errors'), (
            'You must call `.is_valid()` before calling `.save()`.'
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
            discourse_feedback.save()

        else:
            discourse_feedback.update(feedback, feedback_metadata)

        return discourse_feedback


class FeedbackSerializers(ModelSerializer):
    class Meta:
        model = Feedback
        fields = ["application", "feedback_id", "parent_feedback", "title", "description", "impact"]

