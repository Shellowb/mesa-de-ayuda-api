from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'API.settings')

app = Celery('API')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks() 

#beat settings
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')



app.conf.beat_schedule = {
    # Executes every Monday morning at 7:30 a.m.
    'add-every-minute': {
        'task': 'tasks.send_today_notifications',
        'schedule': crontab(minute=1)
    },
        'add-every-m': {
        'task': 'tasks.add',
        'schedule': crontab(minute=1),
        'args': (16, 16),
    },
}
