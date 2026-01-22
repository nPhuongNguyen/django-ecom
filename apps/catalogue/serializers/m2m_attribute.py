from rest_framework import serializers

from ..models.products import M2MAttribute
class M2MAtrributeCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = M2MAttribute
        fields =['attribute', 'attribute_value']

class M2MAtrributeListSerializer(serializers.ModelSerializer):

    class Meta:
        model = M2MAttribute
        fields =['attribute', 'attribute_value']

class M2MAtrributeDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = M2MAttribute
        fields =['attribute', 'attribute_value']