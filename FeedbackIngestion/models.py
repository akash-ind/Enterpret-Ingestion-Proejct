from django.db import models, transaction
from DiscourseIngestion.constants import Constants

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
        (Constants.source, 'Discourse')
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
