from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated


# Create your views here.

@permission_classes([IsAuthenticated])
class TransactionApiView(APIView):
    def post(self, request):
        return Response({'message': 'success'})
