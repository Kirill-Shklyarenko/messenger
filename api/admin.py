from django.contrib import admin

from .models import Account, Message


# Register your models here.
@admin.register(Account)
class UserInstanceAdmin(admin.ModelAdmin):
    list_display = ('username', 'telegram', 'viber', 'whatsapp',)
    # date_hierarchy = 'date_check'
    # list_filter = ('need_check',)
    # fields = ('security', 'shortname',  'emitent_title', )
    # search_fields = ('security', 'price', )
    # prepopulated_fields = {'slug': ('title',)}
    # raw_id_fields = ('security', )
    # ordering = ['status', 'publish']
    # form = UserForm
    # exclude = ('status', )


@admin.register(Message)
class MessageInstanceAdmin(admin.ModelAdmin):
    list_display = ('sender', 'status', 'deferred_time', 'timestamp',)
    readonly_fields = ('status',)
    ordering = ['-timestamp']
