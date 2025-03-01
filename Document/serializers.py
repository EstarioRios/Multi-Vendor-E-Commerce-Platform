from rest_framework import serializers
from .models import Blog, Comment, OrderCard, Card


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


class OrderCardSerializer(serializers.ModelSerializer):
    """
    Serializer for the OrderCard model.
    This serializer converts OrderCard model instances into JSON format and vice versa.
    It includes all fields of the OrderCard model.
    """

    class Meta:
        """
        Meta class for the OrderCardSerializer.
        Defines metadata for the serializer.
        """

        model = OrderCard  # Specifies the model to be serialized
        fields = "__all__"  # Includes all fields of the model in the serialized output


class CardSerializer(serializers.ModelSerializer):
    """
    Serializer for the Card model.
    This serializer converts Card model instances into JSON format and vice versa.
    It includes all fields of the Card model.
    """

    class Meta:
        """
        Meta class for the CardSerializer.
        Defines metadata for the serializer.
        """

        model = Card  # Specifies the model to be serialized
        fields = "__all__"  # Includes all fields of the model in the serialized output
