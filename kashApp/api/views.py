
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import HttpResponse, JsonResponse
from .serializers import UserSerializer
from app.models import AppUser, Category


@api_view(['GET'])
def getdata(request):
    users = AppUser.objects.all()
    serializer = UserSerializer(users, many=True)
    print(serializer.data)
    return Response(serializer.data)