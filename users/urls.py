from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import *

urlpatterns = [
    path('', UserListAPI.as_view(), name='userlist'),
    path('signup/', CreateUserAPI.as_view(), name='signup'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('signup/', UserSignupAPI.as_view(), name='signup'),
]