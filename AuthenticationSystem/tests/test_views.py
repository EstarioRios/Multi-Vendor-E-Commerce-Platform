from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from models import CustomUser
from serializers import CustomUserSerializer_Full
from rest_framework_simplejwt.tokens import RefreshToken


class ViewsTest(TestCase):
    def setUp(self):
        # Create a test client
        self.client = APIClient()

        # Create a test user (customer)
        self.customer = CustomUser.objects.create_customer(
            username="test_customer",
            password="password123",
            first_name="John",
            last_name="Doe",
        )

        # Create a test user (store owner)
        self.store_owner = CustomUser.objects.create_store_owner(
            username="test_store_owner",
            password="password123",
            first_name="Store",
            last_name="Owner",
            store_name="My Store",
            industry="Electronics",
        )

        # Generate tokens for the test users
        self.customer_tokens = RefreshToken.for_user(self.customer)
        self.store_owner_tokens = RefreshToken.for_user(self.store_owner)

    # ----------------------
    # Signup View Tests
    # ----------------------

    def test_signup_customer(self):
        """Test customer signup with valid data"""
        url = reverse("signup")
        data = {
            "username": "new_customer",
            "password": "new_password123",
            "first_name": "New",
            "last_name": "Customer",
            "user_type": "customer",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("success", response.data)
        self.assertIn("tokens", response.data)
        self.assertIn("user", response.data)

    def test_signup_store_owner(self):
        """Test store owner signup with valid data"""
        url = reverse("signup")
        data = {
            "username": "new_store_owner",
            "password": "new_password123",
            "first_name": "New",
            "last_name": "Store Owner",
            "store_name": "New Store",
            "industry": "Fashion",
            "user_type": "store_owner",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("success", response.data)
        self.assertIn("tokens", response.data)
        self.assertIn("user", response.data)

    def test_signup_missing_fields(self):
        """Test signup with missing required fields"""
        url = reverse("signup")
        data = {
            "username": "new_customer",
            "password": "new_password123",
            "user_type": "customer",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    # ----------------------
    # Login Manual View Tests
    # ----------------------

    def test_login_manual_success(self):
        """Test manual login with valid credentials"""
        url = reverse("login_manual")
        data = {
            "username": "test_customer",
            "password": "password123",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("success", response.data)
        self.assertIn("tokens", response.data)
        self.assertIn("user", response.data)

    def test_login_manual_invalid_credentials(self):
        """Test manual login with invalid credentials"""
        url = reverse("login_manual")
        data = {
            "username": "test_customer",
            "password": "wrong_password",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("error", response.data)

    # ----------------------
    # Login JWT View Tests
    # ----------------------

    def test_login_jwt_success(self):
        """Test JWT login with valid token"""
        url = reverse("login_JWT")
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.customer_tokens.access_token}"
        )
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["value"], True)

    def test_login_jwt_invalid_token(self):
        """Test JWT login with invalid token"""
        url = reverse("login_JWT")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer invalid_token")
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["value"], False)

    # ----------------------
    # User Information View Tests
    # ----------------------

    def test_user_information_authenticated(self):
        """Test user information view with authenticated user"""
        url = reverse("user_information")
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.customer_tokens.access_token}"
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("user_data", response.data)

    def test_user_information_unauthenticated(self):
        """Test user information view without authentication"""
        url = reverse("user_information")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
