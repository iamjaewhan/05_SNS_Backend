from django.shortcuts import render
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import CreateUserSerializer, BaseUserSerializer
from .serializers import *

# Create your views here.

class UserSignupAPI(APIView):
    serializer_class = UserSignupSerializer
    
    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            new_user = serializer.save()
            return Response({"user": BaseUserSerializer(new_user).data}, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
