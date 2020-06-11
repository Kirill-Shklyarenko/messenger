from rest_framework import viewsets, mixins, generics, status
from rest_framework.response import Response

from .models import Account, Message
from .serializers import UserSerializer, MessageSerializer


class UserViewSet(generics.ListAPIView,
                  viewsets.ViewSet):
    queryset = Account.objects.all()
    serializer_class = UserSerializer


class MessageViewSet(generics.ListAPIView,
                     mixins.CreateModelMixin,
                     viewsets.ViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    http_method_names = ['get', 'post']

    # @action(detail=False, methods=['post'])
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        new_serializer_data = {
            "status": serializer.data['status'],
        }
        return Response(new_serializer_data, status=status.HTTP_201_CREATED)
