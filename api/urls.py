from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from .views import MessageViewSet

api_info = openapi.Info(
    title="Messenger API",
    default_version='v1.0.0',
    description="""
    
    Useful links:
    =============
    - [Admin](admin/)
    
    Note!
    -----
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
    - Or without []:
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ...
    "recipients": {
        "username": "Snow",
        "service": "whatsapp"
      },
    ...
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    """,
    contact=openapi.Contact(email="shklyara94@gmail.com"),
)

schema_view = get_schema_view()

urlpatterns = [
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='swagger'),
    path('api/sendmsg/', MessageViewSet.as_view({'post': 'create'}), name='sendmsg')

]
