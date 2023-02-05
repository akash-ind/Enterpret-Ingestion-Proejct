from django.urls import path
from DiscourseIngestion.views import DiscourseFeedbackView

app_name = "discourse_ingestion"

urlpatterns = [
    path('ingest/', DiscourseFeedbackView.as_view()),
]
