from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer


class CreateUserSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('email', 'password') 

class BaseUserSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'email')