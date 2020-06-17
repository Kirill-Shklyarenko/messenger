from celery import shared_task

from .models import Message


@shared_task(bind=True,
             name='Send Message',
             max_retries=3,
             soft_time_limit=20)
def send_message_task(self):
    print()


@shared_task(bind=True,
             name='Message checker',
             max_retries=3,
             soft_time_limit=20)
def task_checker(self):
    for messages in Message.objects.all():
        print()
