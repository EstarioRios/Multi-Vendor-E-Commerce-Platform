from rest_framework import serializers
from .models import CustomUser


# Serializer for retrieving all fields of the CustomUser model
class CustomUserSerializer_Full(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"


# Serializer for retrieving store-specific fields
class Stores_List(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "store_name",
            "store_logo",
            "store_industry",
            "store_description",
            "username",
        ]


# Serializer for retrieving customer-specific fields
class Customer_List(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "username"]
