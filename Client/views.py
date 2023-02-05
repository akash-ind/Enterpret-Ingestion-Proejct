from django.shortcuts import render
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.generics import GenericAPIView
from Client.serializers import ApplicationSerializer, ClientSerializer
from Client.models import Application, Client
from rest_framework import status
from rest_framework import permissions
from Enterpret.permissions import Permission


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
    permission_classes = [permissions.IsAuthenticated]

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


class RegisterUser(GenericAPIView):
    serializer_class = ClientSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            client = serializer.save()
            data = serializer.data
            token, created = Token.objects.get_or_create(user=client)
            data['token'] = token.key
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
