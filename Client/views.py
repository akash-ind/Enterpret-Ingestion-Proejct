from django.shortcuts import render
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.generics import GenericAPIView
from Client.serializers import ApplicationSerializer
from Client.models import Application, Client
from rest_framework import status


# Create your views here.

class GetAuthToken(ObtainAuthToken):
    # POST username and password to get token

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })


class ApplicationViewSet(ModelViewSet):
    serializer_class = ApplicationSerializer

    def get_queryset(self):
        client = self.request.user
        applications = Application.objects.filter(client_id=client.id)
        return applications

    def perform_create(self, serializer):
        client = self.request.user
        serializer.save(client_id=client.id)

    def perform_update(self, serializer):
        client = self.request.user
        serializer.save(client_id=client.id)

    def get(self, request, application_id,  *args, **kwargs):
        # Get all the Application by user.
        applications = self.get_queryset()
        applications = applications.get(id=application_id)
        serializer = self.get_serializer()
        serialized_applications = serializer(applications)
        return Response(serialized_applications, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        application_serializer = self.get_serializer()

        serializer = application_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApplicationListView(GenericAPIView):
    serializer_class = ApplicationSerializer

    def get_queryset(self):
        client = self.request.user
        applications = Application.objects.filter(client__id=client.id)
        return applications

    def get(self, request, application_id,  *args, **kwargs):
        # Get all the Application by user.
        applications = self.get_queryset()
        applications = applications.get(id=application_id)
        serializer = self.get_serializer()
        serialized_applications = serializer(applications)
        return Response(serialized_applications, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        application_serializer = self.get_serializer()

        serializer = application_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)