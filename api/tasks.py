import datetime as dt

import pytz
from celery import shared_task, states
from django.db import transaction

from .models import Message


@shared_task(bind=True,
             name='Send Message',
             ignore_result=True,
             default_retry_delay=30 * 60,  # retry in 30 minutes
             autoretry_for=(Exception,),
             retry_backoff=True,
             retry_kwargs={'max_retries': 5})
@transaction.non_atomic_requests
def send_message_task(self, message_pk):
    self.update_state(state=states.PENDING, info=None)
    message = Message.objects.get(pk=message_pk)
    message.status = 2
    message.save()
    self.update_state(state=states.SUCCESS)
    return 'SUCCESS'


@shared_task(bind=True,
             name='Message checker',
             time_limit=60,
             ignore_result=True)
@transaction.non_atomic_requests
def message_checker_task(self):
    utc = pytz.UTC
    for message in Message.objects.all():
        if message.status != 2:
            if message.deferred_time:
                deffered_time = message.deferred_time.replace(second=0, microsecond=0,
                                                              tzinfo=utc)
                datetime_now = dt.datetime.now().replace(second=0, microsecond=0, tzinfo=utc)
                if deffered_time <= datetime_now:
                    send_message_task.apply_async(args=(message.pk,))
                    self.update_state(state=states.PENDING, info=None)
            else:
                send_message_task.apply_async(args=(message.pk,))
                self.update_state(state=states.PENDING, info=None)
    self.update_state(state=states.SUCCESS)
    return 'SUCCESS'
