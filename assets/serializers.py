from rest_framework import serializers
from .models import Vehicle


class VehicleSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Vehicle
        fields = [
            'id',
            'owner',
            'name',
            'registration_number',
            'vehicle_type',
            'make',
            'model',
            'year',
            'fuel_type',
            'capacity_kg',
            'status',
            'notes',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'owner', 'created_at', 'updated_at']
