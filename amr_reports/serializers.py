from rest_framework import serializers
from .models import LabResult  # remove Facility if it doesn't exist

class LabResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabResult
        fields = '__all__'
