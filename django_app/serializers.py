from rest_framework import serializers
from drf_braces.serializers.form_serializer import FormSerializer
from .models import SpSolvedModel, SpSimulationVariablesModel
from .forms import SPSimulationVariables


class SpSolvedModelSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = SpSolvedModel
        fields = '__all__'


class SPSimulationVariablesModelSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = SpSimulationVariablesModel
        fields = '__all__'
