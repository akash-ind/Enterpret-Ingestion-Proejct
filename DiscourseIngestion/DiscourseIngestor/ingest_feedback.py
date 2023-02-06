from DiscourseIngestion.DiscourseIngestor.fetch import FetchDiscourseFeedback
from DiscourseIngestion.models import DiscourseFeedback
from Registration.models import DiscourseRegistration


class IngestDiscourseFeedback:

    def ingest(self, application_id):
        data = FetchDiscourseFeedback().get(application_id)
        for post in data.get("posts"):
            discourse_feedback = DiscourseFeedback.transform_api_data(post, application_id)
            try:
                discourse_feedback.save()
            except Exception as e:
                print(e)


def ingest_job():
    application_ids = DiscourseRegistration.objects.filter(
        integration_type=DiscourseRegistration.PULL_MODEL
    ).values_list('app_id', flat=True)
    ingest_discourse_feedback = IngestDiscourseFeedback()
    for application_id in application_ids:
        ingest_discourse_feedback.ingest(application_id)
