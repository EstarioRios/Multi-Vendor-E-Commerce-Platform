# tests_models.py
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import Permission
from models import CustomUser, CustomUserManager
from Product.models import Industry  # Assuming Industry model exists in Product app
import os


# Helper function to create test image file
def create_test_image():
    return SimpleUploadedFile(
        "test_logo.jpg", b"file_content", content_type="image/jpeg"
    )


class CustomUserModelTest(TestCase):
    def setUp(self):
        # Create test industry for store owner tests
        self.industry = Industry.objects.create(name="Electronics")

        # Common valid data for user creation
        self.base_user_data = {
            "first_name": "John",
            "last_name": "Doe",
            "username": "johndoe",
            "password": "securepassword123",
        }

    # ----------------------
    # CustomUserManager Tests
    # ----------------------

    def test_create_customer_success(self):
        """Test successful customer creation with required fields"""
        user = CustomUser.objects.create_customer(
            **self.base_user_data, phone_number="+989123456789"
        )
        self.assertEqual(user.user_type, "customer")
        self.assertTrue(user.check_password("securepassword123"))

    def test_create_customer_missing_required_field(self):
        """Test validation for missing required fields in customer creation"""
        with self.assertRaises(ValueError):
            CustomUser.objects.create_customer(
                first_name="John",
                # Missing last_name
                username="johndoe",
                password="password",
            )

    def test_create_store_owner_with_valid_data(self):
        """Test successful store owner creation with all required fields"""
        user = CustomUser.objects.create_store_owner(
            **self.base_user_data,
            phone_number="+989123456789",
            store_name="Tech World",
            industry=self.industry,
            store_logo=create_test_image()
        )
        self.assertEqual(user.user_type, "store_owner")
        self.assertEqual(user.store_name, "Tech World")
        self.assertTrue(user.store_logo.name.startswith("store_logos/"))

    def test_create_admin_with_temporary_password(self):
        """Test admin creation with auto-generated temporary password"""
        # Mock SMS service if needed
        user = CustomUser.objects.create_admin(
            **self.base_user_data,
            phone_number="+989123456789",
            national_code="1234567890"
        )
        self.assertTrue(user.check_password(user.password))  # Temporary password check
        self.assertEqual(user.user_type, "admin")

    # ------------------
    # Validator Tests
    # ------------------

    def test_phone_number_validation(self):
        """Test phone number regex validator"""
        user = CustomUser(**self.base_user_data, phone_number="invalid")
        with self.assertRaises(ValidationError):
            user.full_clean()

    def test_national_code_validation(self):
        """Test national code validator"""
        user = CustomUser(
            **self.base_user_data, phone_number="+989123456789", national_code="123"
        )
        with self.assertRaises(ValidationError):
            user.full_clean()

    def test_store_logo_validation(self):
        """Test file type and size validation for store logo"""
        invalid_file = SimpleUploadedFile(
            "test_logo.txt", b"file_content", content_type="text/plain"
        )
        user = CustomUser.objects.create_store_owner(
            **self.base_user_data,
            phone_number="+989123456789",
            store_name="Tech World",
            industry=self.industry,
            store_logo=invalid_file
        )
        with self.assertRaises(ValidationError):
            user.full_clean()

    # ------------------
    # Model Method Tests
    # ------------------

    def test_string_representation(self):
        """Test __str__ method returns username"""
        user = CustomUser.objects.create_customer(
            **self.base_user_data, phone_number="+989123456789"
        )
        self.assertEqual(str(user), "johndoe")

    def test_user_permissions_relationship(self):
        """Test M2M relationship with Permission model"""
        user = CustomUser.objects.create_customer(
            **self.base_user_data, phone_number="+989123456789"
        )
        permission = Permission.objects.get(codename="view_customuser")
        user.user_permissions.add(permission)
        self.assertIn(permission, user.user_permissions.all())

    def tearDown(self):
        # Clean up uploaded files
        for user in CustomUser.objects.all():
            if user.store_logo:
                if os.path.isfile(user.store_logo.path):
                    os.remove(user.store_logo.path)
