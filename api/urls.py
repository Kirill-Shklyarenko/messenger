from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import routers

from .views import MessageViewSet, UserViewSet

router = routers.DefaultRouter()
router.register(r'recipient', UserViewSet, basename='recipient')
router.register(r'message', MessageViewSet, basename='message')

api_info = openapi.Info(
    title="Messenger API",
    default_version='v1',
    description="""
    
    #### Useful links:
    - [Admin](admin/)
    - [Clean DRF](api/)
    
    """,
    contact=openapi.Contact(email="shklyara94@gmail.com"),
)

schema_view = get_schema_view()

urlpatterns = [
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/', include(router.urls)),
    # path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

]
