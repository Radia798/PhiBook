from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import UserRegisterForm, UserProfileForm, PostForm, CommentForm
from .models import Post, Comment
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Order, Post
from .serializers import OrderSerializer,PostSerializer
import requests
from django.conf import settings

# Registration
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Account created! Please log in.")
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'main/register.html', {'form': form})

# Login
from django.contrib.auth.forms import AuthenticationForm
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'main/login.html', {'form': form})

# Logout
def user_logout(request):
    logout(request)
    return redirect('login')

# Dashboard
@login_required
def dashboard(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'main/dashboard.html', {'posts': posts})

# Add Post
@login_required
def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('dashboard')
    else:
        form = PostForm()
    return render(request, 'main/add_post.html', {'form': form})

# My Posts
@login_required
def my_posts(request):
    posts = Post.objects.filter(user=request.user)
    return render(request, 'main/my_posts.html', {'posts': posts})

# Edit Post
@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('my_posts')
    else:
        form = PostForm(instance=post)
    return render(request, 'main/edit_post.html', {'form': form})

# Delete Post
@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)
    post.delete()
    return redirect('my_posts')

# Like/Unlike
@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect('dashboard')

# Add Comment
@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
    return redirect('dashboard')

# Edit Comment
@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = CommentForm(instance=comment)
    return render(request, 'main/edit_comment.html', {'form': form})

# Delete Comment
@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)
    comment.delete()
    return redirect('dashboard')

# Edit Profile
@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = UserProfileForm(instance=request.user.userprofile)
    return render(request, 'main/edit_profile.html', {'form': form})

# @api_view(['POST'])
# def create_order(request):
#     serializer = OrderSerializer(data=request.data)
#     if serializer.is_valid():
#         order = serializer.save()
#         return Response({
#             "message": "Order created",
#             "order_id": order.id
#         })
#     return Response(serializer.errors)



# @api_view(['POST'])
# def initiate_payment(request):
#     order_id = request.data.get("order_id")

#     url = "https://sandbox.sslcommerz.com/gwprocess/v4/api.php"

#     data = {
#         "store_id": "your_store_id",
#         "store_passwd": "your_store_password",
#         "total_amount": 499,
#         "currency": "BDT",
#         "tran_id": str(order_id),
#         "success_url": "http://localhost:5173/success",
#         "fail_url": "http://localhost:5173/fail",
#         "cancel_url": "http://localhost:5173/cancel",
#         "cus_name": "Customer",
#         "cus_email": "test@mail.com",
#         "cus_phone": "01700000000",
#         "cus_add1": "Dhaka",
#         "cus_city": "Dhaka",
#         "cus_country": "Bangladesh",
#         "shipping_method": "NO",
#         "product_name": "PhiBook Premium",
#         "product_category": "Subscription",
#         "product_profile": "general",
#     }

#     response = requests.post(url, data=data)
#     return Response(response.json())


@api_view(["GET"])
def get_posts(request):
    posts = Post.objects.all().order_by("-created_at")
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def create_order(request):
    serializer = OrderSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Order created successfully"})

    return Response(serializer.errors)