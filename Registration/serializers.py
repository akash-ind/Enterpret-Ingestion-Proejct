from rest_framework import serializers
from Registration.models import PlayStoreRegistration, TwitterRegistration, DiscourseRegistration


class RegistrationSerializer(serializers.ModelSerializer):
    app_name = serializers.SlugRelatedField(read_only=True, slug_field='app_name')


class PlayStoreRegistrationSerializer(RegistrationSerializer):
    class Meta:
        model = PlayStoreRegistration
        fields = ['application', 'access_id', 'secret_key', 'integration_type']
        extra_kwargs = {
            'secret_key': {'write_only': True}
        }


class TwitterRegistrationSerializer(RegistrationSerializer):
    class Meta:
        model = TwitterRegistration
        fields = ['application', 'access_id', 'secret_key', 'integration_type']
        extra_kwargs = {
            'secret_key': {'write_only': True}
        }


class DiscourseRegistrationSerializer(RegistrationSerializer):
    class Meta:
        model = DiscourseRegistration
        fields = ['application', 'access_id', 'secret_key', 'integration_type']
        extra_kwargs = {
            'secret_key': {'write_only': True}
        }


class IntercomRegistrationSerializer(RegistrationSerializer):
    class Meta:
        model = DiscourseRegistration
        fields = ['application', 'access_id', 'secret_key', 'integration_type']
        extra_kwargs = {
            'secret_key': {'write_only': True}
        }