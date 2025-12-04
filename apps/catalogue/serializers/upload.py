from rest_framework import serializers
from django.core.validators import FileExtensionValidator
class UploadImageSerializer(serializers.Serializer):
    list_image = serializers.ListField(
        child=serializers.FileField(
            validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])],
        ),
    )