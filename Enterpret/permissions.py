from Client.models import Application
from django.http import HttpResponseBadRequest


class Permission:

    @staticmethod
    def is_client_authorised(request, application_id):
        client = request.user
        if not Application.objects.filter(client_id=client.id).exists():
            raise HttpResponseBadRequest("Application cannot be accessed")
