from django.shortcuts import render
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.serializers import BaseUserSerializer
from .serializers import *
from .models import *
from .utils.permissions import *


# Create your views here.
class PostListAPI(APIView):
    serializer_class = PostSerializer
    
    def get(self, request):
        res = {}
        post_queryset = Post.objects.all()
        serializer = PostSerializer(post_queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    @transaction.atomic()
    def post(self, request):
        permission_classes = [IsAuthenticated]
        
        posted_user = get_user_model().objects.get(pk=request.user.id)
        new_post = Post.objects.create(title=request.data['title'], content=request.data['content'], user=posted_user)
        for hashtag in request.data['hashtag']:
            new_tag, is_created = Hashtag.objects.get_or_create(tag=hashtag)
            new_post.hashtag.add(new_tag)
        new_post.save()
        serializer = PostSerializer(new_post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PostDetailAPI(APIView):
    permission_classes = [IsOwnerOrReadOnly]
    
    def get(self, request, post_id):
        try:
            post_queryset = Post.objects.get(pk=post_id)
            serializer = PostSerializer(post_queryset)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    
    @transaction.atomic()
    def delete(self, request, post_id):
        try:
            post = Post.objects.get(pk=post_id)
            if self.check_object_permissions(request, post):
                post.delete()
                return Response(status=status.HTTP_200_OK)
            return Response( status=status.HTTP_401_UNAUTHORIZED)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic()
    def patch(self, request, post_id):
        try:
            post = Post.objects.get(pk=post_id)
            if self.check_object_permissions(request, post):
                post.title = request.data.get('title', post.title)
                post.content = request.data.get('content', post.content)  
                post.hashtag.clear()
                for hashtag in request.data['hashtag']:
                    new_tag, is_created = Hashtag.objects.get_or_create(tag=hashtag)
                    post.hashtag.add(new_tag)
                post.save()
                serializer = PostSerializer(post)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic()
    def put(self, request, post_id):
        try:
            post = Post.deleted_objects.get(pk=post_id)
            if self.check_object_permissions(request, post):
                post.restore()
                serializer = PostSerializer(post)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    
