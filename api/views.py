from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser

from .models import User
from .serializers import UserSerializer


# Create your views here.
class ArticleViewSet(viewsets.ModelViewSet):
    # method or 'methods' can be skipped because the action only handles a single method (GET)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # @swagger_auto_schema(operation_description='GET /articles/today/')
    # @action(detail=False, methods=['get'])
    # def today(self, request):
    #     breakpoint()
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
