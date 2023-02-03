from django.db import models


# Create your models here.

class Registration(models.Model):
    PULL_MODEL = 'P01'
    PUSH_MODEL = 'P02'

    INTEGRATION_TYPE_CHOICES = [
        (PULL_MODEL, 'PULL MODEL'),
        (PUSH_MODEL, 'PUSH MODEL')
    ]
    app = models.ForeignKey('Client.Application', on_delete=models.CASCADE)
    access_id = models.CharField(max_length=5000, null=True)
    secret_key = models.CharField(max_length=5000, null=True)
    integration_type = models.CharField(choices=INTEGRATION_TYPE_CHOICES, max_length=3)

    class Meta:
        abstract = True


class PlayStoreRegistration(Registration):
    """
    Some other Play store specific keys and values which will help in connecting
    to play store and fetch reviews
    """
    pass


class TwitterRegistration(Registration):
    """
    Some other Twitter specific keys and values which will help in connecting
    to Twitter and fetch reviews
    """
    pass


class DiscourseRegistration(Registration):
    """
    Some other Discourse specific keys which helps to connect to Discourse
    """
    pass
