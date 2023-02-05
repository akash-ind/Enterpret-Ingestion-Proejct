from django.db import models, transaction


# Create your models here.
class TwitterFeedback(models.Model):
    SOURCE = 'S01'
    pass


class IntercomFeedback(models.Model):
    SOURCE = 'S02'

    pass


class PlaystoreFeedback(models.Model):
    SOURCE = 'S03'

    review_id = models.BigIntegerField(null=True, blank=True)
    username = models.TextField(null=True, blank=True)
    review_title = models.TextField(null=True, blank=True)
    review_description = models.TextField(null=True, blank=True)
    ratings = models.IntegerField(null=True, blank=True)


class DiscourseFeedback(models.Model):
    """
    Feedback ingested from Discourse
    """
    SOURCE = 'S04'

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
        return "-".join([self.SOURCE, post_id])

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
        feedback_metadata.application = self.application
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
        discourse_feedback.updated_at_discourse = data.get('updated_at', discourse_feedback.created_at_discourse)
        return discourse_feedback


class Feedback(models.Model):
    """
    Main Model containing feedbacks from various sources
    Will be used for processing data and performing analytics
    """
    application = models.ForeignKey('Client.Application', on_delete=models.CASCADE)
    feedback_id = models.CharField(max_length=5000, primary_key=True)
    # We will use it for maintaining the relationship to the parent review, or conversation
    parent_feedback = models.ForeignKey('FeedbackIngestion.Feedback', on_delete=models.SET_NULL, null=True, blank=True)

    title = models.TextField(null=True, blank=True)
    description = models.TextField()
    impact = models.IntegerField()  # todo: Check if the naming is correct

    class Meta:
        ordering = ("-feedback_id", )

    def __str__(self):
        return self.title


class FeedbackMetadata(models.Model):
    """
    For a feedback, MetaData about the feedback
    """
    source_choices = [
        ('playstore', 'PlayStore'),
        ('twitter', 'Twitter'),
        ('intercom', 'Intercom'),
        (DiscourseFeedback.SOURCE, 'Discourse')
    ]
    # duplicated as it might improve performance
    application = models.ForeignKey('Client.Application', on_delete=models.CASCADE)
    app_version = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    username = models.TextField(null=True, blank=True)
    source = models.CharField(choices=source_choices, max_length=100)
    feedback = models.ForeignKey('FeedbackIngestion.Feedback', on_delete=models.CASCADE)
    language = models.CharField(max_length=5000, null=True, blank=True)
    # Timestamps at which feedback created or updated on their respective platform
    feedback_created_timestamp = models.DateTimeField()
    feedback_updated_timestamp = models.DateTimeField()


class DiscourseFeedbackInfo(models.Model):
    """
    Model for storing info about the
    last fetched post, so we get posts after this
    in the next hit.
    """
    application = models.ForeignKey('Client.Application', on_delete=models.CASCADE)
    last_post_timestamp = models.DateField()  # get the posts after this timestamp

    @staticmethod
    def get_last_post_timestamp(application_id):
        """
        :param application_id:
        :return: None/DiscourseFeedbackInfo
        """
        return DiscourseFeedbackInfo.objects.filter(application__id=application_id) \
            .order_by('-last_post_timestamp') \
            .first()
