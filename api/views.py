from django.db import IntegrityError
from rest_framework import viewsets, generics, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import exception_handler

from .models import Message
from .serializers import MessageSerializer


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
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
                     generics.ListAPIView,
                     ):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    http_method_names = ['post']

    @action(detail=False, methods=['post'])
    def sendmsg(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = {
            "message_text": serializer.validated_data['text'],
            "message_recipients": serializer.validated_data['recipients'],
            "message_status": "NEW",
        }
        return Response(response, status=status.HTTP_201_CREATED)
