import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery()
app.config_from_object('django.conf:settings', namespace='CELERY')


app.conf.beat_schedule = {

    'every minute': {
        'task': 'Message checker',
        'schedule': 60.0,
    },

}

app.autodiscover_tasks()
