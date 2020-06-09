from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
# class DocsView(APIView):
#     """ OLOLLlol

#     1) For viewing data in json (EndPoint №1)
#     3) Just for confortable preview (paginated by 100 elements on the page)
#     """
#
#     def get(self, request, *args, **kwargs):
#         apidocs = {'1)View all data in json': request.build_absolute_uri('api/json/'),
#                    }
#         return Response(apidocs)
