# celery.py

import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bills.settings')

app = Celery("bills")
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
# app.autodiscover_tasks('billsManager')

app.conf.beat_schedule = {
    'send-bill-reminders-daily': {
        'task': 'billsManager.tasks.send_bill_reminders',
        'schedule': crontab(hour=8, minute=0),  # Adjust the time as needed
    },
}