from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile, Post, Comment

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['location', 'phone', 'profile_pic']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['text', 'image', 'youtube_url']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']