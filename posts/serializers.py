from django.contrib.auth import get_user_model

from rest_framework.serializers import ModelSerializer

from .models import *
from users.serializers import BaseUserSerializer


class HashtagSerializer(ModelSerializer):
    class Meta:
        model = Hashtag
        fields = '__all__'
        
    def create(self, validated_data):
        ModelClass = self.Meta.model
        
        try:
            instance = ModelClass._default_manager.get_or_create(**validated_data)
            return instance
        except IntegrityError:
            raise IntegrityError
            
        
class PostSerializer(ModelSerializer):
    user = BaseUserSerializer()
    hashtag = HashtagSerializer(many=True)
        
    class Meta:
        model = Post
        fields = '__all__'
        depth = 1            
        
        
class PostHashtagSerializer(ModelSerializer):
    post = PostSerializer()
    hashtag = HashtagSerializer
    
    class Meta:
        model = PostHashtag
        fields = '__all__'
        depth = 2
        
        

        