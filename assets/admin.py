from django.contrib import admin
from .models import Driver, Vehicle


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'license_number', 'license_expiry', 'owner', 'status', 'created_at']
    list_filter = ['status']
    search_fields = ['name', 'license_number', 'phone', 'owner__username']


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ['name', 'registration_number', 'vehicle_type', 'owner', 'status', 'current_driver', 'created_at']
    list_filter = ['status', 'fuel_type', 'vehicle_type']
    search_fields = ['name', 'registration_number', 'owner__username']
