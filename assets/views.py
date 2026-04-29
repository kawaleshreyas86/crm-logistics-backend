from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Vehicle
from .serializers import VehicleSerializer


class VehicleViewSet(viewsets.ModelViewSet):
    """
    Full CRUD for Vehicles.
    A user can only see and manage their own vehicles.
    """
    serializer_class = VehicleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Scopes every action to the currently authenticated user
        return Vehicle.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        # Automatically assigns the logged-in user as the owner
        serializer.save(owner=self.request.user)
