from django.shortcuts import render
from django.db import transaction
from django.db.models import Q
from django.core.paginator import Paginator
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
        #해시태그 필터링
        filter_condition = Q()
        
        if 'filtering' in request.GET.keys():
            filter_tags = request.GET['filtering'].split(',')
            filter_tags = list(map(lambda x:'^([0-9a-zA-Z]+\,)*%s(,[0-9a-zA-Z]+)*$'%x, filter_tags))
            for tag in filter_tags:
                filter_condition.add(Q(tags__iregex=tag), Q.AND)
            
        post_hashtag_queryset = PostHashtagSetView.objects.filter(filter_condition)
        
        if 'searching' in request.GET.keys():
            searching_key = request.GET['searching']
            post_hashtag_queryset = post_hashtag_queryset.filter(Q(post__title__icontains=searching_key)|Q(post__content__icontains=searching_key))
       
        post_objs = list(map(lambda x:x.post, post_hashtag_queryset))[::-1]

        serializer = PostSerializer(post_objs, many=True)
        p = Paginator(serializer.data, request.GET.get('pagination', 10))
        requested_page = p.get_page(request.GET.get('page',1))
        res = {
            "current_page":requested_page.number,
            "previous_page":requested_page.previous_page_number() if requested_page.has_previous() else requested_page.start_index(),
            "next_page": requested_page.next_page_number() if requested_page.has_next() else requested_page.end_index(), 
            "posts":requested_page.object_list
        }
        return Response(res, status=status.HTTP_200_OK)
        
    
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
    
class LikeUserPostAPI(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic()
    def put(self, request, post_id):
        like_queryset = LikeUserPost.objects.filter(user=request.user.id, post=post_id)
        if len(like_queryset) > 0:
            like_queryset.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            LikeUserPost.objects.create(user=request.user.id, post=post.id)
            return Response(status=status.HTTP_201_CREATED)
        

