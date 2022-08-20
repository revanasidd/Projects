from post.views import *
from django.urls import path

urlpatterns = [
    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/', LoginAPI.as_view(), name='login'),
    path('post/create/', PostCreateView.as_view(), name='post-create'),
    path('user/follow/', FallowUser.as_view(), name='user-follow'),
    path('post/like/', UserLikedPost.as_view(), name='post-like'),
    path('user/posts/', PostLists.as_view(), name='posts'),


]