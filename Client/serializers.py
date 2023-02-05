from rest_framework.serializers import ModelSerializer
from Client.models import Application, Client

class ApplicationSerializer(ModelSerializer):
    class Meta:
        model = Application
        fields = ['app_name']


class ClientSerializer(ModelSerializer):
    class Meta:
        model = Client
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'company_name']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def save(self, **kwargs):
        assert hasattr(self, '_errors'), (
            'You must call `.is_valid()` before calling `.save()`.'
        )

        assert not self.errors, (
            'You cannot call `.save()` on a serializer with invalid data.'
        )

        password = self.validated_data.pop('password')

        instance = super().save(**kwargs)
        instance.set_password(password)
        instance.save()
        return instance
