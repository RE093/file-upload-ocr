from rest_framework import serializers


class UploadFileSerializer(serializers.Serializer):
    files = serializers.FileField()
    connection_id = serializers.CharField()

    required_fields = ['file', 'connection_id']