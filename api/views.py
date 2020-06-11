from rest_framework import viewsets

from .models import Account, Message
from .serializers import UserSerializer, MessageSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = UserSerializer

    # @swagger_auto_schema(operation_description='GET /users/')
    # @action(detail=False, methods=['get'])
    # def get_all_users(self, request):
    #     return self.queryset
    #
    # @swagger_auto_schema(method='get', operation_description="GET /articles/{id}/image/")
    # @swagger_auto_schema(method='post', operation_description="POST /articles/{id}/image/")
    # @action(detail=True, methods=['get', 'post'], parser_classes=(MultiPartParser,))
    # def image(self, request, id=None):
    #     breakpoint()
    #
    # @swagger_auto_schema(operation_description="PUT /articles/{id}/")
    # def update(self, request, *args, **kwargs):
    #     breakpoint()
    #
    # @swagger_auto_schema(operation_description="PATCH /articles/{id}/")
    # def partial_update(self, request, *args, **kwargs):
    #     breakpoint()


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
