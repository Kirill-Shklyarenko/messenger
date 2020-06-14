from django.contrib import admin

from .models import Message, Recipient


# Register your models here.
@admin.register(Message)
class MessageInstanceAdmin(admin.ModelAdmin):
    list_display = ('status', 'deferred_time',)


@admin.register(Recipient)
class RecipientInstanceAdmin(admin.ModelAdmin):
    list_display = ('username', 'service',)
