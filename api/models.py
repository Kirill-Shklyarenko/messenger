import uuid

from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Account(models.Model):
    username = models.CharField(max_length=25, unique=True, blank=True, null=True)
    telegramm = models.SlugField(blank=True, unique=True, null=True)
    viber = models.SlugField(blank=True, unique=True, null=True)
    whatsapp = models.SlugField(blank=True, unique=True, null=True)

    def __str__(self):
        return self.username


class Message(models.Model):
    STATUS = [
        ('DEFFERED', 'Deffered'),
        ('SENDING', 'Sending'),
        ('DELIVERED', 'Delivered'),
        ('FAILED', 'FAILED'),
        ('WAITING', 'waiting'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    message = models.TextField()
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='Sender')
    status = models.CharField(max_length=10, choices=STATUS)
    deffered_time = models.DateTimeField(null=True, blank=True)
    receivers_list = models.ManyToManyField(Account)
    telegramm = models.BooleanField(default=False)
    viber = models.BooleanField(default=False)
    whatsapp = models.BooleanField(default=False)

# class Messenger(models.Model):
#     msg = models.OneToOneField('Message',
#                                on_delete=models.CASCADE,
#                                null=True)
#     telegramm = models.BooleanField(default=False)
#     viber = models.BooleanField(default=False)
#     whatsapp = models.BooleanField(default=False)
#
#     def __str__(self):
#         return f'{self.telegramm}{self.viber}{self.whatsapp}'
