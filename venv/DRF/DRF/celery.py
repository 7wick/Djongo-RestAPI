from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DRF.settings')

app = Celery('DRF')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'add-every-20-seconds': {
        'task': 'length_username_periodic',
        'schedule': 20.0,
        # 'args': (16, 4)
    },

    # 'add-every-minute-contrab': {
    #     'task': 'multiply_two_numbers',
    #     'schedule': crontab(),
    #     'args': (16, 16),
    # },

}

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


# -------------------------------------------------------------
# Your backend (Redis or RabbitMQ recommended).
# celeryd (the worker that runs your tasks)
# celerybeat (if you want periodic tasks)
# celerycam (if you want to dump those tasks into the Django ORM)

#=============================================
# COMMANDS:
# celery -A DRF beat -l info                      #to run beat
# celery -A DRF worker -l info -P eventlet        #to run celery worker
# redis-server                                            #to run redis server

# https://github.com/codingforentrepreneurs/Guides/blob/master/all/Celery_Redis_with_Django.md