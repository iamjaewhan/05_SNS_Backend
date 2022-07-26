from django.urls import path

from .views import *

urlpatterns = [
    path('', PostListAPI.as_view(), name='posts'),
    path('<int:post_id>/', PostDetailAPI.as_view(), name='post_detail'),
]