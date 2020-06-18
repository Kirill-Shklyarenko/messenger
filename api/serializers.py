from rest_framework import serializers

from api.models import Message, Recipient


class RecipientSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(default=None,
                                  read_only=True)

    class Meta:
        model = Recipient
        fields = ('id', 'username', 'service')
        # validators = [
        #     serializers.UniqueTogetherValidator(
        #         queryset=model.objects.all(),
        #         fields=('id', 'username', 'service'),
        #         message=f"This user is exist"
        #                 f"Unique constraint Failed in RecipientSerializer"
        #     )
        # ]


class MessageSerializer(serializers.ModelSerializer):
    text = serializers.CharField(required=True)
    recipients = RecipientSerializer(required=True)
    deferred_time = serializers.DateTimeField(required=False, allow_null=True)

    class Meta:
        model = Message
        fields = ('text', 'recipients', 'deferred_time',)

    def create(self, validated_data):
        recipient_validated_data = validated_data.pop('recipients')
        recipient = Recipient.objects.get_or_create(**recipient_validated_data)
        validated_data.update(dict(recipients=recipient[0]))
        return Message.objects.create(**validated_data)
