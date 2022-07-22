from django.shortcuts import render
from django.contrib.auth import get_user_model, authenticate

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .serializers import *

# Create your views here.
class UserListAPI(APIView):
    """
    유저 리스트 조회 api - 삭제 예정
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        users = get_user_model().objects.all()
        serializer = BaseUserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserSignupAPI(APIView):
    serializer_class = UserSignupSerializer
    
    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            new_user = serializer.save()
            return Response({"user": BaseUserSerializer(new_user).data}, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
        
        
class UserLoginAPI(APIView):
    serializer_class = UserLoginSerializer
    
    def post(self, request):
        user = authenticate(email=request.data.get('email'), password=request.data.get('password'))
        if user is not None:
            serializer = BaseUserSerializer(user)
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res_data = {
                "user": serializer.data,
                "access_token": access_token,
                "refresh_token": refresh_token,
            }
            return Response(data=res_data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
            