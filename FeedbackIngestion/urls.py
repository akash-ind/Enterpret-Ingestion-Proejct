from django.urls import path
from FeedbackIngestion.views import FeedbackListView

urlpatterns = [
    path('feedback/', FeedbackListView.as_view()),
]