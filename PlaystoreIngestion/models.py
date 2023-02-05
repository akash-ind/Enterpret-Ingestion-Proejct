from django.db import models, transaction
from FeedbackIngestion.models import BaseIngestion, FeedbackMetadata, Feedback
from Enterpret.constants import Constants
# Create your models here.


class PlaystoreFeedback(BaseIngestion):
    SOURCE = Constants.playstore_source

    application = models.ForeignKey('Client.Application', on_delete=models.CASCADE)
    app_version = models.CharField(max_length=100, null=True, blank=True)
    review_id = models.CharField(max_length=100)
    parent_review_id = models.CharField(max_length=100, null=True, blank=True)
    username = models.TextField(null=True, blank=True)
    title = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    ratings = models.IntegerField(null=True, blank=True)
    created_at_playstore = models.DateTimeField(null=True, blank=True)
    updated_at_playstore = models.DateTimeField(null=True, blank=True)

    def get_review_id(self, review_id):
        """
        Concatenation of source and post_id
        :return:str
        """
        return "-".join([self.SOURCE, str(self.application_id), str(review_id)])

    def sync_feedback(self, feedback):
        """
        :param feedback: Feedback
        :return: Feedback
        """
        feedback.feedback_id = self.get_review_id(self.review_id)
        feedback.application = self.application
        if self.parent_review_id:
            feedback.parent_feedback_id = self.get_review_id(self.parent_review_id)
        feedback.title = self.title
        feedback.description = self.description
        feedback.impact = self.ratings
        return feedback

    def sync_feedback_metadata(self, feedback_metadata):
        """
        :param feedback_metadata: FeedbackMetadata
        :return: FeedbackMetadata
        """
        feedback_metadata.source = self.SOURCE
        feedback_metadata.username = self.username
        feedback_metadata.feedback_id = self.get_review_id(self.review_id)
        feedback_metadata.language = 'english'  # Can be optimised with coding for languages
        feedback_metadata.app_version = self.app_version
        feedback_metadata.feedback_created_timestamp = self.created_at_playstore
        feedback_metadata.feedback_updated_timestamp = self.updated_at_playstore or self.created_at_playstore
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

            playstore_feedback_info = PlaystoreFeedbackInfo()
            playstore_feedback_info.application_id = self.application_id
            playstore_feedback_info.last_post_timestamp = self.created_at_playstore
            playstore_feedback_info.save()

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

            playstore_feedback_info = PlaystoreFeedbackInfo()
            playstore_feedback_info.application_id = self.application_id
            playstore_feedback_info.last_post_timestamp = self.updated_at_playstore
            playstore_feedback_info.save()

    @staticmethod
    def transform_api_data(data, application_id):
        """
        :param application_id: The application we are adding data to
        :param data: API data Dict
        :return: DiscourseFeedback
        """
        playstore_feedback = PlaystoreFeedback()
        playstore_feedback.application_id = application_id
        playstore_feedback.review_id = data.get('id')
        playstore_feedback.username = data.get('username')
        playstore_feedback.title = data.get('topic_title_headline')
        playstore_feedback.description = data.get('blurb')
        playstore_feedback.ratings = data.get('ratings')
        playstore_feedback.created_at_playstore = data.get('created_at')
        playstore_feedback.updated_at_playstore = data.get('updated_at', playstore_feedback.created_at_playstore)
        return playstore_feedback


class PlaystoreFeedbackInfo(models.Model):
    """
    Contains info about the ingested rows of feedback from playstore
    """

    application = models.ForeignKey('Client.Application', on_delete=models.CASCADE)
    last_post_timestamp = models.DateTimeField()  # get the posts after this timestamp

    @staticmethod
    def get_last_post_timestamp(application_id):
        """
        :param application_id:
        :return: None/DiscourseFeedbackInfo
        """
        return PlaystoreFeedbackInfo.objects.filter(application__id=application_id) \
            .order_by('-last_post_timestamp') \
            .first()
