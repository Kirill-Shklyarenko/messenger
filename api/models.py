import uuid

from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Account(models.Model):
    username = models.CharField(primary_key=True, max_length=25, unique=True)
    telegram = models.SlugField(blank=True, unique=True, null=True)
    viber = models.SlugField(blank=True, unique=True, null=True)
    whatsapp = models.SlugField(blank=True, unique=True, null=True)

    def __str__(self):
        return self.username


class Message(models.Model):
    STATUS = [
        (1, 'New'),
        (2, 'Sended'),
        (3, 'Failed'),
    ]
    status = models.PositiveSmallIntegerField(default=1, choices=STATUS)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    message = models.TextField()
    sender = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='Sender')
    receivers_list = models.ManyToManyField(Account)

    timestamp = models.DateTimeField(auto_now_add=True)
    deferred_time = models.DateTimeField(null=True, blank=True)
    telegram = models.BooleanField(default=False)
    viber = models.BooleanField(default=False)
    whatsapp = models.BooleanField(default=False)

    def __str__(self):
        return self.message

    class Meta:
        ordering = ('timestamp',)
