from rest_framework import serializers
from .models import Product, Industry, MainImage, ProductImage


# Serializer for the MainImage model (to show only the main image)
class MainImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainImage
        fields = [
            "product_image"
        ]  # Only include the product_image field (which contains the main image)


# Serializer for the ProductImage model (to show all images related to a product)
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["image"]  # Include the image field to show all images of the product


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
            "id",  # Unique identifier for the product, used for referencing specific products
            "price",  # Product price, representing the cost of the item
            "main_image",  # Show only the main image
            "active",
        ]


# Serializer for the Industry model
# Converts Industry model instances to JSON format and vice versa
class IndustrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Industry
        fields = "__all__"  # Includes all fields from the Industry model
