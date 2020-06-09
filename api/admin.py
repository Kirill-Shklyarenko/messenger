from django.contrib import admin
from .models import User, Message


# Register your models here.
@admin.register(User)
class UserInstanceAdmin(admin.ModelAdmin):
    list_display = ('name', 'telegram', 'viber', 'whatsapp',)
    # date_hierarchy = 'date_check'
    # list_filter = ('need_check',)
    # fields = ('security', 'shortname',  'emitent_title', )
    # search_fields = ('security', 'price', )
    # prepopulated_fields = {'slug': ('title',)}
    # raw_id_fields = ('security', )
    # ordering = ['status', 'publish']


@admin.register(Message)
class MessageInstanceAdmin(admin.ModelAdmin):
    list_display = ('sender_id', 'status', 'is_sended',
                    'receivers_list', 'messengers_list', 'deffered_time')
