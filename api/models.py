from django.db import models


# Create your models here.


class User(models.Model):
    id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=75,
                            null=True,
                            blank=False)
    telegram = models.SlugField(blank=True,
                                null=True)
    viber = models.SlugField(blank=True,
                             null=True)
    whatsapp = models.SlugField(blank=True,
                                null=True)


class Message(models.Model):
    STATUS = [
        (0, 'Deffered...'),
        (1, 'Sending...'),
        (2, 'Delivered!'),
        (3, 'FAILED!!!'),
        (4, 'WARNING!!'),
    ]
    id = models.UUIDField(primary_key=True)
    sender_id = models.ForeignKey(User,
                                  related_name='Sender',
                                  on_delete=models.CASCADE)
    message = models.TextField()
    status = models.PositiveSmallIntegerField(choices=STATUS)
    is_sended = models.BooleanField(default=False)
    receivers_list = models.ManyToManyField(User,
                                            related_name='List of receivers+',
                                            limit_choices_to=('id', 'name'),
                                            blank=True)
    messengers_list = models.ManyToManyField(User,
                                             related_name='List of messengers to use+',
                                             limit_choices_to=('telegram',
                                                               'viber',
                                                               'whatsapp'),
                                             blank=True)
    deffered_time = models.DateTimeField(null=True, blank=True)
