from django.contrib import admin
from .models import Vehicle


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ['name', 'registration_number', 'vehicle_type', 'owner', 'status', 'created_at']
    list_filter = ['status', 'fuel_type', 'vehicle_type']
    search_fields = ['name', 'registration_number', 'owner__username']
