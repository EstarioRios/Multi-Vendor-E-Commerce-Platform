from rest_framework import serializers
from .models import Product


# Serializer for full product details
class ProductSerializerFull(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"  # Includes all fields from the Product model


# Serializer for displaying limited product details
class ProductSerializerShow(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "title",  # Product title
            "descriptions",  # Product description
            "industry",  # Associated industry
        ]
