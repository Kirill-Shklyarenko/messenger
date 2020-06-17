import datetime as dt

import pytz
from celery import shared_task
from django.db import transaction

from .models import Message


@shared_task(bind=True,
             name='Send Message',
             max_retries=3,
             soft_time_limit=20)
@transaction.atomic  # Cause DB can lock if several tasks will get same object
def send_message_task(self, message_pk):  # noqa
    message = Message.objects.get(pk=message_pk)
    print(f'Try to send {message} with STATUS = {message.status}')
    message.status = 2
    message.save()
    print(f'{message} DELIVERED')


@shared_task(bind=True,
             name='Message checker')
def message_checker_task(self):  # noqa
    utc = pytz.UTC
    for message in Message.objects.all():
        # This for deferred_time
        if message.deferred_time:
            deffered_time = message.deferred_time.replace(second=0, microsecond=0, tzinfo=utc)
            datetime_now = dt.datetime.now().replace(second=0, microsecond=0, tzinfo=utc)
            if deffered_time <= datetime_now:
                send_message_task.apply_async(args=(message.pk,))
        # This for failed messages
        if message.status != 2:
            send_message_task.apply_async(args=(message.pk,))
