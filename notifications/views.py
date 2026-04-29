from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated

from .models import AlertRule
from .serializers import AlertRuleSerializer

class AlertRuleViewSet(viewsets.ModelViewSet):
    """
    ViewSet for full CRUD operations and managing alert rules.
    """
    serializer_class = AlertRuleSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Automatically scopes all actions to the current user
        return AlertRule.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
