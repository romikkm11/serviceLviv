from rest_framework import serializers
from .models import Service

class ServiceSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source="company.name", read_only=True)
    company_logo_url = serializers.CharField(source="company.logo_url", read_only=True)
    company_url = serializers.CharField(source="company.company_url", read_only=True)
    service_type_name = serializers.CharField(source="service_type.name", read_only=True)
    service_general_name = serializers.CharField(source="service_general_name.name", read_only=True)
    service_general_name_id = serializers.IntegerField(source="service_general_name.id", read_only=True)
    class Meta:
        model = Service
        fields = '__all__'