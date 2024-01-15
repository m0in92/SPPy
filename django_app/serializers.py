from rest_framework import serializers
from drf_braces.serializers.form_serializer import FormSerializer
from .models import EcmSimulationVariablesModel, EcmSolvedModel, SpSolvedModel, SpSimulationVariablesModel
from .forms import SPSimulationVariables


class EcmSimulationVariablesModelSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = EcmSimulationVariablesModel
        fields = '__all__'


class EcmSolvedModelSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = EcmSolvedModel
        fields = '__all__'


class SpSolvedModelSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = SpSolvedModel
        fields = '__all__'


class SpSimulationVariablesModelSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = SpSimulationVariablesModel
        fields = '__all__'
