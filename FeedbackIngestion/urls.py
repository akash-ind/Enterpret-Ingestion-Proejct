from django.urls import path
from FeedbackIngestion.views import DiscourseFeedbackView, FeedbackListView

urlpatterns = [
    path('discourse/', DiscourseFeedbackView.as_view()),
    path('feedback/', FeedbackListView.as_view()),
]