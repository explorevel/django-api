from rest_framework import serializers
from .models import *

class InstitutionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = institutions
        fields = '__all__'
        # fields = ['symbol', 'top_buyer', 'amount']

class MetadataSerializer(serializers.ModelSerializer):
    class Meta:
        model = metadata
        fields = '__all__'

class ReportsSerializer(serializers.ModelSerializer):
    class Meta:
        model = reports
        fields = '__all__'