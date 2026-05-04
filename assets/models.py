from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Driver(models.Model):
    """
    Represents a driver belonging to an Owner (User).
    An owner can have multiple drivers independent of their vehicle count.
    A driver is assigned to at most one vehicle at a time (enforced via
    the reverse OneToOne on Vehicle.driver).
    """

    STATUS_CHOICES = [
        ('available', 'Available'),   # Free, not assigned to any vehicle
        ('active', 'Active'),          # Currently assigned to a vehicle
        ('inactive', 'Inactive'),      # On leave / terminated / unavailable
    ]

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='drivers',
        help_text="The owner (user) this driver belongs to"
    )
    name = models.CharField(max_length=255, help_text="Full name of the driver")
    phone = models.CharField(max_length=20, help_text="Primary contact number")
    license_number = models.CharField(
        max_length=50,
        unique=True,
        help_text="Driving license number"
    )
    license_expiry = models.DateField(help_text="License expiry date")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='available'
    )
    notes = models.TextField(blank=True, null=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    joining_date = models.DateField(null=True, blank=True)
    account_number = models.CharField(max_length=50, blank=True)
    ifsc_code = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.license_number}) — {self.get_status_display()}"


class Vehicle(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('maintenance', 'Under Maintenance'),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vehicles')
    vehicle_number = models.CharField(max_length=50, unique=True)
    vehicle_type = models.CharField(max_length=100, help_text="e.g. Truck, Van, Bike")
    brand = models.CharField(max_length=100, blank=True)
    model = models.CharField(max_length=100, blank=True, help_text="Model name e.g. 407, Prima")
    year = models.PositiveIntegerField(null=True, blank=True)
    location = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    driver = models.OneToOneField(
        Driver,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='vehicle',
        help_text="The driver currently assigned to this vehicle"
    )
    purchase_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    purchase_date = models.DateField(null=True, blank=True)
    chassis_number = models.CharField(max_length=100, blank=True)
    engine_number = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.vehicle_number} - {self.owner.username}"
