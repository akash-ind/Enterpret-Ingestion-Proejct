from django.shortcuts import render
from rest_framework.viewsets import GenericViewSet
from Registration.models import PlayStoreRegistration, TwitterRegistration, DiscourseRegistration
from Registration.serializers import PlayStoreRegistrationSerializer
from rest_framework.response import Response
from rest_framework import status


# Create your views here.


class PlayStoreRegistrationViewSet(GenericViewSet):
    serializer_class = PlayStoreRegistrationSerializer

    def get_queryset(self):
        user = self.request.user
        return PlayStoreRegistration.objects.filter(app__client__id=user.id)

    def get(self, request, *args, **kwargs):
        playstore_registrations = self.get_queryset()
        if kwargs.get('registration_id'):
            playstore_registrations = playstore_registrations.filter(id=kwargs.get('registration_id'))
        playstore_registrations_serializer = self.get_serializer()
        serializer = playstore_registrations_serializer(data=playstore_registrations, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """
        Create a registration with access id and secret id for an App
        :return:
        """
        playstore_registrations_serializer = self.get_serializer()
        serializer = playstore_registrations_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
