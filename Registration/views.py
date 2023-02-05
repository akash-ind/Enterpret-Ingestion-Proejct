from django.shortcuts import render
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from Registration.models import PlayStoreRegistration, TwitterRegistration, DiscourseRegistration, IntercomRegistration
from Registration.serializers import PlayStoreRegistrationSerializer, DiscourseRegistrationSerializer, IntercomRegistrationSerializer, TwitterRegistrationSerializer
from rest_framework import permissions
from Enterpret.permissions import Permission


# Create your views here.


class PlayStoreRegistrationViewSet(ModelViewSet):
    serializer_class = PlayStoreRegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        client = self.request.user
        return PlayStoreRegistration.objects.filter(app__client_id=client.id)

    def perform_update(self, serializer):
        if Permission.is_client_authorised(self.request, self.request.data.get('app_id')):
            serializer.save()

    def perform_create(self, serializer):
        if Permission.is_client_authorised(self.request, self.request.data.get('app_id')):
            serializer.save()


class TwitterRegistrationViewSet(ModelViewSet):
    serializer_class = TwitterRegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        client = self.request.user
        return TwitterRegistration.objects.filter(app__client_id=client.id)

    def perform_update(self, serializer):
        if Permission.is_client_authorised(self.request, self.request.data.get('app_id')):
            serializer.save()

    def perform_create(self, serializer):
        if Permission.is_client_authorised(self.request, self.request.data.get('app_id')):
            serializer.save()


class DiscourseRegistrationViewSet(ModelViewSet):
    serializer_class = DiscourseRegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        client = self.request.user
        return DiscourseRegistration.objects.filter(app__client_id=client.id)

    def perform_update(self, serializer):
        if Permission.is_client_authorised(self.request, self.request.data.get('app_id')):
            serializer.save()

    def perform_create(self, serializer):
        if Permission.is_client_authorised(self.request, self.request.data.get('app_id')):
            serializer.save()


class IntercomRegistrationViewSet(ModelViewSet):
    serializer_class = IntercomRegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        client = self.request.user
        return IntercomRegistration.objects.filter(app__client_id=client.id)

    def perform_update(self, serializer):
        if Permission.is_client_authorised(self.request, self.request.data.get('app_id')):
            serializer.save()

    def perform_create(self, serializer):
        if Permission.is_client_authorised(self.request, self.request.data.get('app_id')):
            serializer.save()