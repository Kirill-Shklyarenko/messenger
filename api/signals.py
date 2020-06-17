from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Message
from .tasks import send_message_task


@receiver(post_save, sender=Message, dispatch_uid='send_message')
def send_message(instance, created, **kwargs):  # noqa
    if instance.deferred_time is None and created:
        transaction.on_commit(lambda: send_message_task.apply_async(args=(instance.pk,)))
