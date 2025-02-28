from rest_framework import serializers
from .models import Blog, Comment


# Serializer to return all fields of a blog post
class BlogFullSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = "__all__"  # Includes all fields from the Blog model


# Serializer to show only selected fields of a blog post
class BlogSerializerShow(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ["title", "description"]  # Returns only title and description


# Serializer for comments
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment  # Fixed: Changed from Blog to Comment
        fields = "__all__"  # Includes all fields from the Comment model
