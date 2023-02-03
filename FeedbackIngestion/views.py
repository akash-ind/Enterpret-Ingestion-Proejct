from django.shortcuts import render
from rest_framework.viewsets import GenericViewSet
from FeedbackIngestion.models import DiscourseFeedback, Feedback
from FeedbackIngestion.serializers import DiscourseFeedbackSerializer
from rest_framework.response import Response
from rest_framework import status
# Create your views here.


class DiscourseFeedbackViewSet(GenericViewSet):
    serializer_class = DiscourseFeedbackSerializer

    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        """
        Push Model where we are giving APIs to push the Feedback
        into database.
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        data = request.data
        serializer = DiscourseFeedbackSerializer(request.data)

        if serializer.is_valid():
            # idempotency supported by using primary key from the data
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


