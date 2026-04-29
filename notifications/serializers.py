from rest_framework import serializers
from .models import AlertRule

class AlertRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlertRule
        fields = ['id', 'user', 'title', 'message', 'task_date', 'remind_before_days', 'has_triggered', 'created_at']
        read_only_fields = ['id', 'created_at', 'has_triggered']

    def create(self, validated_data):
        # Automatically set user to the requesting user if not provided, though it's better handled in perform_create in viewset
        return super().create(validated_data)
