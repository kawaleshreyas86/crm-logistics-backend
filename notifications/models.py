from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    alert_rule = models.ForeignKey('AlertRule', on_delete=models.SET_NULL, null=True, blank=True, related_name='notifications')
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Notification for {self.user.username}: {self.title}"

class AlertRule(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='alert_rules')
    title = models.CharField(max_length=255)
    message = models.TextField()
    task_date = models.DateField()
    remind_before_days = models.PositiveIntegerField(default=0)
    has_triggered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Alert for {self.user.username}: {self.title} on {self.task_date}"
