from datetime import timedelta

CELERYBEAT_SCHEDULE = {
    'add-every-30-seconds': {
        'task': 'sureroute.tasks.test_sureroute',
        'schedule': timedelta(seconds=60),
        'args': ()
    },
}
BROKER_URL = "redis://localhost:6379/0"
