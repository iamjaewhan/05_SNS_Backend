from django.urls import path

from .views import *

urlpatterns = [
    path('', PostListAPI.as_view(), name='posts'),
    path('test/', TestAPI.as_view()),
]