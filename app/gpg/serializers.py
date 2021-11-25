from rest_framework import serializers


class GpgSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=255)
    passphrase = serializers.CharField(max_length=200)
