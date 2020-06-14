import uuid

from django.db import models


# Create your models here.
class Recipient(models.Model):
    user = models.CharField(primary_key=True, max_length=25, unique=True)
    telegram = models.SlugField(blank=True, unique=True, null=True)
    viber = models.SlugField(blank=True, unique=True, null=True)
    whatsapp = models.SlugField(blank=True, unique=True, null=True)

    def __str__(self):
        return self.user


class Message(models.Model):
    STATUS = [
        (1, 'New'),
        (2, 'Sended'),
        (3, 'Failed'),
    ]
    status = models.PositiveSmallIntegerField(default=1, choices=STATUS)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    text = models.TextField()
    recipient = models.ManyToManyField(Recipient)
    timestamp = models.DateTimeField(auto_now_add=True)

    deferred_time = models.DateTimeField(null=True, blank=True)
    # telegram = models.BooleanField(default=False)
    # viber = models.BooleanField(default=False)
    # whatsapp = models.BooleanField(default=False)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['-timestamp']
