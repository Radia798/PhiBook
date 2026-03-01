from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Post, Comment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = fields = ['id', 'user', 'text', 'created_at']

class PostSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id',
            'user',
            'text',
            'image',
            'youtube_url',
            'created_at',
            'likes_count',
            'comments',
        ]

    def get_likes_count(self, obj):
        return obj.likes.count()