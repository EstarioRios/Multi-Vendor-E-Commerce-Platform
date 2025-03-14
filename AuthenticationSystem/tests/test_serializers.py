from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import serializers
from models import CustomUser
from serializers import CustomUserSerializer_Full, Stores_List, Customer_List
from django.core.files.uploadedfile import SimpleUploadedFile


class SerializersTest(APITestCase):
    def setUp(self):
        # Create a test user with store owner role
        self.store_owner = CustomUser.objects.create(
            first_name="Store",
            last_name="Owner",
            username="store_owner",
            password="password123",
            phone_number="+989123456789",
            user_type="store_owner",
            store_name="My Store",
            store_logo=SimpleUploadedFile(
                "logo.jpg", b"file_content", content_type="image/jpeg"
            ),
            store_industry="Electronics",
            store_description="Best electronics store in town!",
        )

        # Create a test user with customer role
        self.customer = CustomUser.objects.create(
            first_name="John",
            last_name="Doe",
            username="johndoe",
            password="password123",
            phone_number="+989987654321",
            user_type="customer",
        )

    # ----------------------
    # CustomUserSerializer_Full Tests
    # ----------------------

    def test_custom_user_serializer_full(self):
        """Test if CustomUserSerializer_Full returns all fields correctly"""
        serializer = CustomUserSerializer_Full(self.store_owner)
        data = serializer.data

        # Check if all fields are present
        self.assertIn("id", data)
        self.assertIn("first_name", data)
        self.assertIn("last_name", data)
        self.assertIn("username", data)
        self.assertIn("phone_number", data)
        self.assertIn("store_name", data)
        self.assertIn("store_logo", data)
        self.assertIn("store_industry", data)
        self.assertIn("store_description", data)

    # ----------------------
    # Stores_List Serializer Tests
    # ----------------------

    def test_stores_list_serializer(self):
        """Test if Stores_List serializer returns store-specific fields"""
        serializer = Stores_List(self.store_owner)
        data = serializer.data

        # Check if only store-specific fields are present
        self.assertEqual(
            list(data.keys()),
            [
                "store_name",
                "store_logo",
                "store_industry",
                "store_description",
                "username",
            ],
        )

        # Check if the data is correct
        self.assertEqual(data["store_name"], "My Store")
        self.assertEqual(data["store_industry"], "Electronics")
        self.assertEqual(data["store_description"], "Best electronics store in town!")
        self.assertEqual(data["username"], "store_owner")

    # ----------------------
    # Customer_List Serializer Tests
    # ----------------------

    def test_customer_list_serializer(self):
        """Test if Customer_List serializer returns customer-specific fields"""
        serializer = Customer_List(self.customer)
        data = serializer.data

        # Check if only customer-specific fields are present
        self.assertEqual(list(data.keys()), ["first_name", "last_name", "username"])

        # Check if the data is correct
        self.assertEqual(data["first_name"], "John")
        self.assertEqual(data["last_name"], "Doe")
        self.assertEqual(data["username"], "johndoe")
