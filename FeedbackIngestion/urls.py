from django.urls import path
from FeedbackIngestion.views import FeedbackListView

urlpatterns = [
    path('list/', FeedbackListView.as_view()),
]