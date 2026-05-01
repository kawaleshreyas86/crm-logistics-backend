from rest_framework import serializers
from .models import Driver, Vehicle


class DriverSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)
    # Expose the assigned vehicle registration number (if any) as a read-only hint
    assigned_vehicle_registration = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Driver
        fields = [
            'id',
            'owner',
            'name',
            'phone',
            'license_number',
            'license_expiry',
            'status',
            'assigned_vehicle_registration',
            'notes',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'owner', 'status', 'created_at', 'updated_at']

    def get_assigned_vehicle_registration(self, obj):
        """Return the registration number of the vehicle this driver is currently assigned to."""
        try:
            return obj.assigned_vehicle.registration_number
        except Vehicle.DoesNotExist:
            return None


class AssignDriverSerializer(serializers.Serializer):
    """Minimal serializer used only for the assign-driver action payload."""
    driver_id = serializers.IntegerField()


class DriverSummarySerializer(serializers.ModelSerializer):
    """Lightweight nested representation of a driver, embedded inside VehicleSerializer."""

    class Meta:
        model = Driver
        fields = ['id', 'name', 'phone', 'license_number', 'status']


class VehicleSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)
    current_driver = DriverSummarySerializer(read_only=True)

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
            'current_driver',
            'notes',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'owner', 'current_driver', 'created_at', 'updated_at']
