from rest_framework.serializers import ModelSerializer
from Client.models import Application, Client

class ApplicationSerializer(ModelSerializer):
    class Meta:
        model = Application
        fields = ['app_name']


class ClientSerializer(ModelSerializer):
    class Meta:
        model = Client
        fields = ['username', 'first_name', 'last_name', 'email', 'password', ]