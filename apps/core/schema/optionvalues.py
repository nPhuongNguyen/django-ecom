from rest_framework import serializers
from apps.core.models.products import OptionValue
from apps.core.schema.options import OptionSerializer
class OptionValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = OptionValue
        fields = '__all__'

class OptionValueOutputSerializer(serializers.ModelSerializer):
    option = OptionSerializer(read_only = True)

    class Meta:
        model = OptionValue
        fields = '__all__'
