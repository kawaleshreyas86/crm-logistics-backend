from django.db import transaction
from rest_framework import serializers
from datetime import date

from .models import Driver, Vehicle, VehicleDocument


class DriverSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)
    assigned_vehicle_number = serializers.SerializerMethodField(read_only=True)

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
            'assigned_vehicle_number',
            'salary',
            'joining_date',
            'account_number',
            'ifsc_code',
            'notes',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'owner', 'status', 'created_at', 'updated_at']

    def get_assigned_vehicle_number(self, obj):
        try:
            return obj.vehicle.vehicle_number
        except Vehicle.DoesNotExist:
            return None


class DriverSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ['id', 'name', 'phone', 'license_number', 'status']


class VehicleDocumentSerializer(serializers.ModelSerializer):
    vehicle_number = serializers.CharField(source='vehicle.vehicle_number', read_only=True)
    status = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = VehicleDocument
        fields = [
            'id',
            'vehicle',
            'vehicle_number',
            'document_type',
            'document_number',
            'expiry_date',
            'status',
            'file',
            'notes',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'vehicle_number', 'status', 'created_at', 'updated_at']

    def get_status(self, obj):
        if not obj.expiry_date:
            return 'unknown'

        today = date.today()
        days_left = (obj.expiry_date - today).days

        if days_left < 0:
            return 'expired'
        if days_left <= 7:
            return 'due_soon'
        if days_left <= 30:
            return 'expiring_soon'
        return 'valid'

    def validate_vehicle(self, vehicle):
        request = self.context.get('request')
        if request and vehicle.owner_id != request.user.id:
            raise serializers.ValidationError("Vehicle not found or does not belong to you.")
        return vehicle


class VehicleSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)
    driver = DriverSummarySerializer(read_only=True)
    documents = VehicleDocumentSerializer(many=True, read_only=True)
    current_driver = serializers.PrimaryKeyRelatedField(
        source='driver',
        queryset=Driver.objects.all(),
        required=False,
        allow_null=True,
        write_only=True,
    )

    class Meta:
        model = Vehicle
        fields = [
            'id',
            'owner',
            'vehicle_number',
            'vehicle_type',
            'brand',
            'model',
            'year',
            'location',
            'status',
            'driver',
            'current_driver',
            'purchase_price',
            'purchase_date',
            'chassis_number',
            'engine_number',
            'created_at',
            'updated_at',
            'documents',
        ]
        read_only_fields = ['id', 'owner', 'driver', 'created_at', 'updated_at', 'documents']

    def validate_current_driver(self, driver):
        if driver is None:
            return driver

        request = self.context.get('request')
        if request is not None and driver.owner_id != request.user.id:
            raise serializers.ValidationError("Driver not found or does not belong to you.")

        try:
            assigned_vehicle = driver.vehicle
        except Vehicle.DoesNotExist:
            assigned_vehicle = None

        if assigned_vehicle is not None and (self.instance is None or assigned_vehicle.pk != self.instance.pk):
            raise serializers.ValidationError(
                f"Driver '{driver.name}' is already assigned to vehicle '{assigned_vehicle.vehicle_number}'."
            )

        return driver

    def create(self, validated_data):
        driver = validated_data.pop('driver', None)

        with transaction.atomic():
            vehicle = Vehicle.objects.create(driver=driver, **validated_data)
            if driver is not None and driver.status != 'active':
                driver.status = 'active'
                driver.save(update_fields=['status'])

        return vehicle

    def update(self, instance, validated_data):
        driver_provided = 'driver' in validated_data
        new_driver = validated_data.pop('driver', instance.driver)
        old_driver = instance.driver

        with transaction.atomic():
            for attr, value in validated_data.items():
                setattr(instance, attr, value)

            if driver_provided:
                instance.driver = new_driver

            instance.save()

            if driver_provided and old_driver is not None and old_driver != new_driver and old_driver.status != 'available':
                old_driver.status = 'available'
                old_driver.save(update_fields=['status'])

            if driver_provided and new_driver is not None and old_driver != new_driver and new_driver.status != 'active':
                new_driver.status = 'active'
                new_driver.save(update_fields=['status'])

        return instance
