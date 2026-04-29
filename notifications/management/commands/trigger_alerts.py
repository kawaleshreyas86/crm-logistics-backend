from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from notifications.models import AlertRule, Notification

class Command(BaseCommand):
    help = 'Triggers notifications for alert rules whose reminder date has arrived.'

    def handle(self, *args, **options):
        today = timezone.localdate()
        
        alerts = AlertRule.objects.filter(has_triggered=False)
        triggered_count = 0

        for alert in alerts:
            trigger_date = alert.task_date - timedelta(days=alert.remind_before_days)
            
            if today >= trigger_date:
                Notification.objects.create(
                    user=alert.user,
                    alert_rule=alert,
                    title=f"Reminder: {alert.title}",
                    message=alert.message
                )
                alert.has_triggered = True
                alert.save(update_fields=['has_triggered'])
                triggered_count += 1
                
        self.stdout.write(self.style.SUCCESS(f'Successfully triggered {triggered_count} alerts.'))
