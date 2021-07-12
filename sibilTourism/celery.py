import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sibilTourism.settings')

app = Celery('sibilTourism')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
