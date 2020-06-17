from django.contrib import admin

from .models import Message, Recipient


# Register your models here.
@admin.register(Message)
class MessageInstanceAdmin(admin.ModelAdmin):
    list_display = ('text', 'recipients', 'status', 'deferred_time',)

    def recipients(self, obj):
        return obj.recipients.username

    recipients.admin_order_field = 'message__recipient'


@admin.register(Recipient)
class RecipientInstanceAdmin(admin.ModelAdmin):
    list_display = ('username', 'service',)
