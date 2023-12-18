from rest_framework import serializers
from drf_braces.serializers.form_serializer import FormSerializer
from .models import SpModel
from .forms import SPSimulationVariables


class SpModelSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = SpModel
        fields = '__all__'


class SpSimulationVariablesSerializer(FormSerializer):
    class Meta(object):
        form = SPSimulationVariables
