from django.shortcuts import render
from django.db import transaction

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.serializers import BaseUserSerializer

from .serializers import *
from .models import *


# Create your views here.
class PostListAPI(APIView):
    serializer_class = PostSerializer
    
    def get(self, request):
        res = {}
        post_queryset = Post.objects.all()
        serializer = PostSerializer(post_queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
