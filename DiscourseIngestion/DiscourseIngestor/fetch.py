from DiscourseIngestion.models import DiscourseFeedbackInfo
from DiscourseIngestion.constants import Constants
import requests


class FetchDiscourseFeedback:
    url = 'https://meta.discourse.org/search.json'

    def get_query_params(self, starting_date):
        return {
            'page': 1,
            'q': 'after: {}'.format(starting_date)
        }

    def fetch_from_discourse(self, starting_date):
        data = requests.get(self.url, self.get_query_params(starting_date))
        print(data.json())
        return data.json()

    def get(self, application_id):
        last_feedback = DiscourseFeedbackInfo.get_last_post_timestamp(application_id)
        starting_date = Constants.start_date
        if last_feedback is not None:
            starting_date = last_feedback.last_post_timestamp.date()
        return self.fetch_from_discourse(starting_date)
