from rest_framework import serializers
from apps.core.models.products import Option
class OptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Option
        fields = '__all__'
        read_only_fields = ['is_deleted']