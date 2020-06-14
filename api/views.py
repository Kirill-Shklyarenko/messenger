from rest_framework import viewsets, generics, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Message, Recipient
from .serializers import MessageSerializer, RecipientSerializer


class RecipientViewSet(generics.ListAPIView,
                       viewsets.ViewSet):
    queryset = Recipient.objects.all()
    serializer_class = RecipientSerializer
    http_method_names = ['get']


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
        new_serializer_data = {
            "message_text": serializer.validated_data['text'],
            "message_status": "new",
        }
        return Response(new_serializer_data, status=status.HTTP_201_CREATED)
