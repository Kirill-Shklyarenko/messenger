from rest_framework import serializers
from api.models import Recipient, Message


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipient
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField(required=False)
    deferred_time = serializers.DateTimeField(required=False)

    @staticmethod
    def get_status(obj):
        return obj.get_status_display()

    def validate(self, data):
        msg_queryset = Message.objects.filter(text=data['text'],
                                              recipient__in=data['recipient'])
        if msg_queryset.count() != 0:
            raise serializers.ValidationError(f'You want to send '
                                              f'SAME MESSAGE to the SAME USERS.'
                                              f'Sorry, but You can’t do that...')

        # if not data['telegram'] and not data['viber'] and not data['whatsapp']:
        #     raise serializers.ValidationError(f'No one messenger is selected. '
        #                                       f'Please choose at least one messenger')

        return data

    def create(self, validated_data):
        if validated_data.get('viber'):
            validated_data.update(dict(status=3))
        else:
            validated_data.update(dict(status=2))

        recipient_list = validated_data.pop('recipient')
        msg_obj = Message.objects.create(**validated_data)
        msg_obj.recipient.add(*recipient_list)
        return msg_obj

    class Meta:
        model = Message
        fields = '__all__'
