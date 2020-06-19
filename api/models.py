from django.db import models


# Create your models here.
class Recipient(models.Model):
    username = models.CharField(max_length=50, null=False, blank=False)
    SERVICE = [
        ('telegram', 'telegram'),
        ('viber', 'viber'),
        ('whatsapp', 'whatsapp'),
    ]
    service = models.CharField(max_length=8, choices=SERVICE, null=False, blank=False)

    def __str__(self):
        return f'{self.username} {self.service}'

    class Meta:
        unique_together = ('username', 'service',)


class Message(models.Model):
    text = models.TextField()
    recipients = models.ForeignKey(Recipient, related_name='messages',
                                   on_delete=models.CASCADE,
                                   null=False, blank=False)

    STATUS = [
        (1, 'NEW'),
        (2, 'DELIVERED'),
        (3, 'FAILED'),
    ]
    status = models.PositiveSmallIntegerField(default=1, choices=STATUS)
    deferred_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.text

    class Meta:
        unique_together = ('text', 'recipients',)
