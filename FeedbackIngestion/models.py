from django.db import models, transaction
from DiscourseIngestion.constants import Constants


# Create your models here.
class TwitterFeedback(models.Model):
    SOURCE = 'S01'
    pass


class IntercomFeedback(models.Model):
    SOURCE = 'S02'

    pass



class BaseIngestion(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """
        Save the feedback model from this
        :param args:
        :param kwargs:
        :return:
        """

        raise NotImplementedError("Implement to save feedback model transforming the data")

    def update(self, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        :return:
        """
        raise NotImplementedError("Implement to update feedback model transforming the data")

    @staticmethod
    def transform_api_data(*args, **kwargs):
        """
        :param args:
        :param kwargs:
        :return: Class Object
        """
        raise NotImplementedError("Implement to transform the API data to object")


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
        ordering = ("-feedback_id",)

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
        (Constants.source, 'Discourse')
    ]

    # duplicated as it might improve performance
    app_version = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    username = models.TextField(null=True, blank=True)
    source = models.CharField(choices=source_choices, max_length=100)
    feedback = models.OneToOneField('FeedbackIngestion.Feedback', on_delete=models.CASCADE)
    language = models.CharField(max_length=5000, null=True, blank=True)
    # Timestamps at which feedback created or updated on their respective platform
    feedback_created_timestamp = models.DateTimeField()
    feedback_updated_timestamp = models.DateTimeField()
