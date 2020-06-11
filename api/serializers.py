from rest_framework import serializers
from api.models import Account, Message


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField(required=False)
    deferred_time = serializers.DateTimeField(required=False)

    @staticmethod
    def get_status(obj):
        return obj.get_status_display()

    def validate(self, data):
        msg_queryset = Message.objects.filter(message=data['message'],
                                              receivers_list__in=data['receivers_list'])

        if not data['telegram'] and not data['viber'] and not data['whatsapp']:
            raise serializers.ValidationError(f'No one messenger is selected. '
                                              f'Please choose at least one messenger')

        if msg_queryset.count() != 0:
            raise serializers.ValidationError(f'You want to send '
                                              f'the SAME MESSAGE to the SAME USER_list. AGAIN!'
                                              f'You can’t do that...Ay-yay-yay')
        return data

    def create(self, validated_data):
        if validated_data.get('deferred_time'):
            validated_data.update(dict(status=1))
        elif validated_data.get('viber'):
            validated_data.update(dict(status=3))
        else:
            validated_data.update(dict(status=2))

        receivers_list = validated_data.pop('receivers_list')
        msg_obj = Message.objects.create(**validated_data)
        msg_obj.receivers_list.add(*receivers_list)
        return msg_obj

    class Meta:
        model = Message
        fields = '__all__'
