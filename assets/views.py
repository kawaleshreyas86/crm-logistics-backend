from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Driver, Vehicle
from .serializers import (
    AssignDriverSerializer,
    DriverSerializer,
    VehicleSerializer,
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
        return Vehicle.objects.filter(owner=self.request.user).select_related('current_driver')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['post'], url_path='assign-driver')
    def assign_driver(self, request, pk=None):
        """
        POST /assets/vehicles/{id}/assign-driver/
        Body: { "driver_id": <int> }

        Rules:
          - The driver must belong to the same owner as the vehicle.
          - The driver must NOT already be assigned to another vehicle.
            (Force caller to unassign first — explicit control.)
        """
        vehicle = self.get_object()
        serializer = AssignDriverSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        driver_id = serializer.validated_data['driver_id']

        # --- Guard 1: Driver must belong to the same owner ---
        try:
            driver = Driver.objects.get(pk=driver_id, owner=request.user)
        except Driver.DoesNotExist:
            return Response(
                {"detail": "Driver not found or does not belong to you."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # --- Guard 2: Driver must not already be assigned to another vehicle ---
        if hasattr(driver, 'assigned_vehicle'):
            return Response(
                {
                    "detail": (
                        f"Driver '{driver.name}' is already assigned to vehicle "
                        f"'{driver.assigned_vehicle.registration_number}'. "
                        "Please unassign them first."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # --- Guard 3: Vehicle already has a driver? ---
        if vehicle.current_driver is not None:
            return Response(
                {
                    "detail": (
                        f"Vehicle '{vehicle.registration_number}' already has driver "
                        f"'{vehicle.current_driver.name}' assigned. "
                        "Please unassign first."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # --- Atomic assignment ---
        with transaction.atomic():
            vehicle.current_driver = driver
            vehicle.save(update_fields=['current_driver'])
            driver.status = 'active'
            driver.save(update_fields=['status'])

        return Response(VehicleSerializer(vehicle).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='unassign-driver')
    def unassign_driver(self, request, pk=None):
        """
        POST /assets/vehicles/{id}/unassign-driver/

        Removes the current driver from this vehicle and sets the driver
        status back to 'available'.
        """
        vehicle = self.get_object()

        if vehicle.current_driver is None:
            return Response(
                {"detail": "This vehicle has no driver assigned."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        with transaction.atomic():
            driver = vehicle.current_driver
            driver.status = 'available'
            driver.save(update_fields=['status'])
            vehicle.current_driver = None
            vehicle.save(update_fields=['current_driver'])

        return Response(VehicleSerializer(vehicle).data, status=status.HTTP_200_OK)
