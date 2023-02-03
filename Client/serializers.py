from rest_framework.serializers import ModelSerializer
from Client.models import Application, Client

class ApplicationSerializer(ModelSerializer):
    class Meta:
        model = Application
        fields = ['app_name']