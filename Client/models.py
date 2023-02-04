from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class Client(AbstractUser):
    company_name = models.CharField(max_length=255)


class Application(models.Model):
    app_name = models.CharField(max_length=255)
    client = models.ForeignKey('Client.Client', on_delete=models.CASCADE)

    def __str__(self):
        return self.app_name
