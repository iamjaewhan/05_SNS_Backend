from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer


class UserSignupSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('email', 'password') 
    
    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

class BaseUserSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'email')
        
class UserLoginSerializer(ModelSerializer):
    class Meta:
        model =  get_user_model()
        fields = ('email', 'password')