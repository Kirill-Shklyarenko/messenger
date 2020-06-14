from rest_framework import viewsets, generics, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Recipient, Message
from .serializers import UserSerializer, MessageSerializer


class UserViewSet(generics.ListAPIView,
                  viewsets.ViewSet):
    queryset = Recipient.objects.all()
    serializer_class = UserSerializer


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
            "message_id": serializer.data['id'],
            "status": serializer.data['status'],
        }
        return Response(new_serializer_data, status=status.HTTP_201_CREATED)
