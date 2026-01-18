from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count
from .models import RequestLog, SuspiciousIP

@shared_task
def detect_anomalies():
    one_hour_ago = timezone.now() - timedelta(hours=1)
    
    # Check for high request volume (>100/hr)
    logs = RequestLog.objects.filter(timestamp__gte=one_hour_ago).values('ip_address').annotate(count=Count('ip_address'))
    
    for log in logs:
        if log['count'] > 100:
            SuspiciousIP.objects.get_or_create(
                ip_address=log['ip_address'],
                reason="High request volume (>100 requests/hour)"
            )

    # Check for access to sensitive paths
    sensitive_paths = ['/admin', '/login']
    sensitive_logs = RequestLog.objects.filter(timestamp__gte=one_hour_ago, path__in=sensitive_paths)
    for s_log in sensitive_logs:
        SuspiciousIP.objects.get_or_create(
            ip_address=s_log.ip_address,
            reason=f"Accessed sensitive path: {s_log.path}"
        )
