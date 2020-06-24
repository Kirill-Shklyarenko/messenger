from django.db import IntegrityError
from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.views import exception_handler

from .models import Message
from .serializers import MessageSerializer


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        response.data['status_code'] = response.status_code
    if isinstance(exc, IntegrityError) and not response:
        response = Response(
            {
                'message': (f'You want to send '
                            f'SAME MESSAGE to the SAME USERS. '
                            f'Sorry, but You can’t do this...')
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    return response


class MessageViewSet(viewsets.ViewSet,
                     generics.CreateAPIView,
                     ):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        """
        - Example for multiple recipients:
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        ...
        "recipients": [
            {
              "username": "Jhon",
              "service": "telegram"
            },
            {
              "username": "Snow",
              "service": "viber"
            }
          ],
        ...
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        - Example for single recipient:
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        ...
        "recipients": [
            {
              "username": "Jhon",
              "service": "telegram"
            }
          ],
        ...
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        - Or without `[]`:
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        ...
        "recipients": {
            "username": "Snow",
            "service": "whatsapp"
          },
        ...
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        - If no need `deferred_time` just delete string that contains it :
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        {
        ...
        "recipients": {
            "username": "Snow",
            "service": "whatsapp"
          }
        }
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        """

        # Check if recipients is a list
        if isinstance(request.data['recipients'], list):
            recipients = request.data.pop('recipients')
            models = []
            for recipient in recipients:
                # validate each model with one recipient at a time
                request.data['recipients'] = recipient
                serializer = MessageSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                models.append(serializer)
            # Save it only after all recipients are valid.
            # To avoid situations when one recipient has wrong id
            # And you already save previous
            saved_models = [model.save() for model in models]
            result_serializer = MessageSerializer(saved_models, many=True)
            return Response(result_serializer.data)
        # Save message as usual
        serializer = MessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
