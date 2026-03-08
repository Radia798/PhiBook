from django.urls import path,include
from . import views
from .views import create_order, get_posts

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('add_post/', views.add_post, name='add_post'),
    path('my_posts/', views.my_posts, name='my_posts'),
    path('edit_post/<int:post_id>/', views.edit_post, name='edit_post'),
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
    path('like_post/<int:post_id>/', views.like_post, name='like_post'),
    path('add_comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('edit_comment/<int:comment_id>/', views.edit_comment, name='edit_comment'),
    path('delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('api/', include('main.api_urls')),
    path("create-order/", create_order),
    path("posts/", get_posts),
    path("order/", create_order),
    path("api/register/", views.api_register),
]