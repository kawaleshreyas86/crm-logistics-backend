from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Vehicle(models.Model):
    FUEL_TYPE_CHOICES = [
        ('petrol', 'Petrol'),
        ('diesel', 'Diesel'),
        ('electric', 'Electric'),
        ('cng', 'CNG'),
        ('hybrid', 'Hybrid'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('maintenance', 'Under Maintenance'),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vehicles')
    name = models.CharField(max_length=255, help_text="A friendly name or label for the vehicle")
    registration_number = models.CharField(max_length=50, unique=True)
    vehicle_type = models.CharField(max_length=100, help_text="e.g. Truck, Van, Bike")
    make = models.CharField(max_length=100, help_text="Brand/manufacturer e.g. Tata, Ashok Leyland")
    model = models.CharField(max_length=100, help_text="Model name e.g. 407, Prima")
    year = models.PositiveIntegerField()
    fuel_type = models.CharField(max_length=20, choices=FUEL_TYPE_CHOICES, default='diesel')
    capacity_kg = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,
                                      help_text="Load capacity in kilograms")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.registration_number}) - {self.owner.username}"
