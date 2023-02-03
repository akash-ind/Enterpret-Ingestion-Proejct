from FeedbackIngestion.DiscourseIngestor.fetch import FetchDiscourseFeedback
from FeedbackIngestion.models import DiscourseFeedback
from Registration.models import DiscourseRegistration


class IngestDiscourseFeedback:

    # Todo: Optimise for Asynchronous Execution
    def ingest(self, application_id):
        data = FetchDiscourseFeedback().get(application_id)
        for post in data.posts:
            discourse_feedback = DiscourseFeedback.transform(post, application_id)
            discourse_feedback.save()


def ingest_job():
    application_ids = DiscourseRegistration.objects.values_list('app_id', flat=True)
    ingest_discourse_feedback = IngestDiscourseFeedback()
    for application_id in application_ids:
        ingest_discourse_feedback.ingest(application_id)
