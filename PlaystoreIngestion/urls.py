from django.urls import path
from PlaystoreIngestion.views import PlaystoreFeedbackView
app_name = "PlaystoreIngestion"

urlpatterns = [
    path('ingest/', PlaystoreFeedbackView.as_view()),
]