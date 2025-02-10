from rest_framework import serializers
from .models import Product


# Serializer for full product details
# This serializer includes all fields from the Product model for detailed product information
class ProductSerializerFull(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"  # Includes all fields from the Product model


# Serializer for displaying limited product details
# This serializer includes only selected fields for a summarized view of the product
class ProductSerializerShow(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "title",  # Product title, a brief name of the product
            "descriptions",  # Product description, detailed information about the product
            "industry",  # Associated industry, the industry category the product belongs to
            "product_type",  # Product type, indicating whether the product is physical or digital
            "type_of_file",  # File type, relevant for digital products (e.g., PDF, ZIP)
            "size",  # Size of the file for digital products, relevant for digital products only
        ]
