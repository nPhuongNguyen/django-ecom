from rest_framework import serializers
from apps.core.models.collection import Collection



class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = '__all__'
        read_only_fields = ['sku','is_deleted']

class CollectionInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = '__all__'
        read_only_fields = ['is_deleted']