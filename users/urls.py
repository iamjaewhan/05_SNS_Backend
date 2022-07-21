from django.urls import path

from .views import *

urlpatterns = [
    path('', UserListAPI.as_view(), name='userlist'),
    path('signup/', UserSignupAPI.as_view(), name='signup'),
    path('login/', UserLoginAPI.as_view(), name='login'),
]