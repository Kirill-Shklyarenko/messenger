from rest_framework import serializers

from api.models import Message, Recipient


class RecipientSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(default=None,
                                  read_only=True)

    class Meta:
        model = Recipient
        fields = ('id', 'username', 'service')
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=('id', 'username', 'service'),
                message=f"This user is exist"
                        f"Unique constraint Failed in RecipientSerializer"
            )
        ]


class MessageSerializer(serializers.ModelSerializer):
    text = serializers.CharField(required=True)
    recipients = RecipientSerializer(many=True, required=True)
    deferred_time = serializers.DateTimeField(required=False)

    class Meta:
        model = Message
        fields = ('text', 'recipients', 'deferred_time',)
        # validators = [
        #     serializers.UniqueTogetherValidator(
        #         queryset=model.objects.all(),
        #         fields=('text', 'recipients'),
        #         message=(f'You want to send '
        #                  f'SAME MESSAGE to the SAME USERS. '
        #                  f'Sorry, but You can’t do this...')
        #     )
        # ]

    def create(self, validated_data):
        message = None
        recipients = validated_data.pop('recipients')
        for recipient_data in recipients:
            recipients = Recipient.objects.get_or_create(**recipient_data)
            validated_data.update(dict(recipients=recipients[0]))
            if recipient_data['service'] == 'viber':
                validated_data.update(dict(status=3))  # <-------- This for Fail case
            message = Message.objects.create(**validated_data)
        return message
