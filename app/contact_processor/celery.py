import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'contact_processor.settings')

app = Celery('contact_processor')

app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


app.conf.timezone = 'UTC'