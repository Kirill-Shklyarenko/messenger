from rest_framework import serializers
from api.models import Account, Message


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'
        # read_only_fields = ('id', 'name', 'telegram', 'viber', 'whatsapp', )


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ('status', )
