from rest_framework import serializers
from .models import SpModel

class SpModelSerializer(serializers.ModelSerializer):
    class Meta:
        model: SpModel
        fields: '__all__'
