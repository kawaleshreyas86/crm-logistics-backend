from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Driver, Vehicle, VehicleDocument, Expense
from .serializers import (
    DriverSerializer,
    VehicleSerializer,
    VehicleDocumentSerializer,
    ExpenseSerializer,
)


class DriverViewSet(viewsets.ModelViewSet):
    """
    Full CRUD for Drivers.
    A user can only see and manage their own drivers.
    """
    serializer_class = DriverSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Driver.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class VehicleViewSet(viewsets.ModelViewSet):
    """
    Full CRUD for Vehicles.
    A user can only see and manage their own vehicles.
    """
    serializer_class = VehicleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Vehicle.objects.filter(owner=self.request.user).select_related('driver')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class VehicleDocumentViewSet(viewsets.ModelViewSet):
    """
    Full CRUD for vehicle documents.
    A user can only manage documents of their own vehicles.
    """
    serializer_class = VehicleDocumentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return VehicleDocument.objects.filter(vehicle__owner=self.request.user).select_related('vehicle')

    def perform_create(self, serializer):
        serializer.save()


class ExpenseViewSet(viewsets.ModelViewSet):
    """
    CRUD for vehicle expenses.
    Users can only manage expenses for their own vehicles.
    """
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Expense.objects.filter(vehicle__owner=self.request.user).select_related('vehicle')

    def perform_create(self, serializer):
        serializer.save()