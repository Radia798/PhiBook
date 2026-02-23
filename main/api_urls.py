from django.urls import path
from .api_views import PostListCreateAPI, PostDetailAPI, CommentCreateAPI

urlpatterns = [
    path('posts/', PostListCreateAPI.as_view()),
    path('posts/<int:pk>/', PostDetailAPI.as_view()),
    path('posts/<int:post_id>/comment/', CommentCreateAPI.as_view()),
]