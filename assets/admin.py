from django.contrib import admin
from .models import Driver, Vehicle


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'license_number', 'license_expiry', 'owner', 'status', 'created_at']
    list_filter = ['status']
    search_fields = ['name', 'license_number', 'phone', 'owner__username']


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ['vehicle_number', 'vehicle_type', 'brand', 'location', 'owner', 'status', 'driver', 'created_at']
    list_filter = ['status', 'vehicle_type', 'location']
    search_fields = ['vehicle_number', 'brand', 'model', 'location', 'owner__username']
