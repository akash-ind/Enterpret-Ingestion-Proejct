# Generated by Django 4.1.5 on 2023-02-06 05:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('FeedbackIngestion', '0003_delete_playstorefeedback_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='IntercomFeedback',
        ),
        migrations.DeleteModel(
            name='TwitterFeedback',
        ),
    ]