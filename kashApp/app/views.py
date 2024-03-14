from django.shortcuts import render
import uuid
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import HttpResponse, JsonResponse
from .models import AppUser, Category
from rest_framework import status
from api.serializers import UserSerializer
# Create your views here.

@api_view(['POST'])
def CreateUser(request):
    uid = uuid.uuid4()
    
    request.data['password'] = request.data.get('password')
    request.data['user_id'] = str(uid)
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    try:
        user = AppUser.objects.get(email=request.data.get('email'))
    except AppUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if user.password == request.data.get('password'):
        return Response({"OK": "success"}, status=status.HTTP_200_OK)
    else:
        return Response({"fail": "wrong password"}, status=status.HTTP_200_OK)

    
