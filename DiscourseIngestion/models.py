from django.db import models, transaction
from FeedbackIngestion.models import Feedback, FeedbackMetadata, BaseIngestion
from DiscourseIngestion.constants import Constants
from datetime import datetime


# Create your models here.
class DiscourseFeedback(BaseIngestion):
    """
    Feedback ingested from Discourse
    """
    SOURCE = Constants.source

    application = models.ForeignKey('Client.Application', on_delete=models.CASCADE)
    post_id = models.TextField()
    username = models.TextField(null=True, blank=True)
    title = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    parent_post_id = models.TextField(null=True, blank=True)
    like_count = models.IntegerField(null=True, blank=True)
    created_at_discourse = models.DateTimeField()
    updated_at_discourse = models.DateTimeField(null=True, blank=True)

    def get_post_id(self, post_id):
        """
        Concatenation of source and post_id
        :return:str
        """
        return "-".join([self.SOURCE, str(self.application_id), str(post_id)])

    def sync_feedback(self, feedback):
        """
        :param feedback: Feedback
        :return: Feedback
        """
        feedback.feedback_id = self.get_post_id(self.post_id)
        feedback.application = self.application
        if self.parent_post_id:
            feedback.parent_feedback_id = self.get_post_id(self.parent_post_id)
        feedback.title = self.title
        feedback.description = self.description
        feedback.impact = self.like_count
        return feedback

    def sync_feedback_metadata(self, feedback_metadata):
        """
        :param feedback_metadata: FeedbackMetadata
        :return: FeedbackMetadata
        """
        feedback_metadata.source = self.SOURCE
        feedback_metadata.username = self.username
        feedback_metadata.feedback_id = self.get_post_id(self.post_id)
        feedback_metadata.language = 'english'  # Can be optimised with coding for languages
        feedback_metadata.feedback_created_timestamp = self.created_at_discourse
        feedback_metadata.feedback_updated_timestamp = self.updated_at_discourse or self.created_at_discourse
        return feedback_metadata

    def save(self, *args, **kwargs):
        """
        We call this only if the id does not exist, otherwise will raise an
        exception.
        :param args:
        :param kwargs:
        :return:
        """
        with transaction.atomic():
            feedback = self.sync_feedback(Feedback())
            feedback.save()

            feedback_metadata = self.sync_feedback_metadata(FeedbackMetadata())
            feedback_metadata.save()

            discourse_feedback_info = DiscourseFeedbackInfo()
            discourse_feedback_info.application_id = self.application_id
            discourse_feedback_info.last_post_timestamp = self.created_at_discourse
            print(discourse_feedback_info.last_post_timestamp)
            discourse_feedback_info.save()

    def update(self, feedback, feedback_metadata):
        """

        :param feedback: Feedback
        :param feedback_metadata: FeedbackMetadata
        :return:
        """
        with transaction.atomic():
            feedback = self.sync_feedback(feedback)
            feedback.save()
            feedback_metadata = self.sync_feedback_metadata(feedback_metadata)
            feedback_metadata.save()

            discourse_feedback_info = DiscourseFeedbackInfo()
            discourse_feedback_info.application_id = self.application_id
            discourse_feedback_info.last_post_timestamp = self.updated_at_discourse
            print(discourse_feedback_info.last_post_timestamp)
            discourse_feedback_info.save()

    @staticmethod
    def transform_api_data(data, application_id):
        """
        :param application_id: The application we are adding data to
        :param data: API data Dict
        :return: DiscourseFeedback
        """
        discourse_feedback = DiscourseFeedback()
        discourse_feedback.application_id = application_id
        discourse_feedback.post_id = data.get('id')
        discourse_feedback.username = data.get('username')
        discourse_feedback.title = data.get('topic_title_headline')
        discourse_feedback.description = data.get('blurb')
        discourse_feedback.like_count = data.get('like_count')
        discourse_feedback.created_at_discourse = data.get('created_at')
        print(discourse_feedback.created_at_discourse, data.get('created_at'))

        discourse_feedback.updated_at_discourse = data.get('updated_at', discourse_feedback.created_at_discourse)
        print(discourse_feedback)
        return discourse_feedback


class DiscourseFeedbackInfo(models.Model):
    """
    Model for storing info about the
    last fetched post, so we get posts after this
    in the next hit.
    """
    application = models.ForeignKey('Client.Application', on_delete=models.CASCADE)
    last_post_timestamp = models.DateTimeField()  # get the posts after this timestamp

    @staticmethod
    def get_last_post_timestamp(application_id):
        """
        :param application_id:
        :return: None/DiscourseFeedbackInfo
        """
        return DiscourseFeedbackInfo.objects.filter(application__id=application_id) \
            .order_by('-last_post_timestamp') \
            .first()
