INSTALLED_APPS = [
    # ...
    'ip_tracking',
    'django_ratelimit',
]

MIDDLEWARE = [
    # ... ضع الميدلوير في الأسفل
    'ip_tracking.middleware.IPMiddleware',
]

# Celery Settings
CELERY_BEAT_SCHEDULE = {
    'detect-anomalies-every-hour': {
        'task': 'ip_tracking.tasks.detect_anomalies',
        'schedule': 3600.0,
    },
}
