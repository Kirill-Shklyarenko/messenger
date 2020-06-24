from datetime import datetime

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
    for message in Message.objects.filter(status__in=[1, 3]):
        if message.deferred_time:
            deffered_time = message.deferred_time.replace(second=0, microsecond=0)
            datetime_now = datetime.now(pytz.utc).replace(second=0, microsecond=0)
            if deffered_time <= datetime_now:
                send_message_task.apply_async(args=(message.pk,))
                self.update_state(state=states.PENDING, info=None)
        else:
            send_message_task.apply_async(args=(message.pk,))
            self.update_state(state=states.PENDING, info=None)
    self.update_state(state=states.SUCCESS)
    return 'SUCCESS'
