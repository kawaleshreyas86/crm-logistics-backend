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


class VehicleDocument(models.Model):
    """
    Represents documents associated with a vehicle
    (RC, Insurance, Permit, etc.)
    """

    DOCUMENT_TYPE_CHOICES = [
        ('rc', 'RC Book'),
        ('insurance', 'Insurance'),
        ('permit', 'Permit'),
        ('pollution', 'Pollution Certificate'),
        ('fitness', 'Fitness Certificate'),
        ('other', 'Other'),
    ]

    vehicle = models.ForeignKey(
        'Vehicle',
        on_delete=models.CASCADE,
        related_name='documents',
        help_text="Vehicle this document belongs to"
    )

    document_type = models.CharField(
        max_length=50,
        choices=DOCUMENT_TYPE_CHOICES
    )

    document_number = models.CharField(
        max_length=100,
        help_text="Document identifier (RC number, policy number, etc.)"
    )

    expiry_date = models.DateField()

    file = models.FileField(
        upload_to='vehicle_documents/',
        null=True,
        blank=True,
        help_text="Uploaded document file (PDF/image)"
    )

    notes = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['expiry_date']
        unique_together = ('vehicle', 'document_type')

    def __str__(self):
        return f"{self.vehicle.vehicle_number} - {self.get_document_type_display()}"

    @property
    def status(self):
        if not self.expiry_date:
            return "unknown"

        today = date.today()
        days_left = (self.expiry_date - today).days

        if days_left < 0:
            return "expired"
        elif days_left <= 7:
            return "due_soon"
        elif days_left <= 30:
            return "expiring_soon"
        else:
            return "valid"
