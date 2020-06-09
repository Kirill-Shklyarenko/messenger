from django.db import models


# Create your models here.
class User(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True)
    name = models.CharField(max_length=75,
                            null=True,
                            blank=False)
    telegram = models.SlugField(blank=True,
                                null=True)
    viber = models.SlugField(blank=True,
                             null=True)
    whatsapp = models.SlugField(blank=True,
                                null=True)

    def __str__(self):
        return self.name
