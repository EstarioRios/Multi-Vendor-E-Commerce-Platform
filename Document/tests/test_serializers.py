from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import serializers
from models import Blog, Comment, Card, OrderCard
from serializers import (
    BlogFullSerializer,
    BlogSerializerShow,
    CommentSerializer,
    CardSerializer,
    OrderCardSerializer,
)
from Product.models import Product
from AuthenticationSystem.models import CustomUser
from django.core.files.uploadedfile import SimpleUploadedFile


class SerializersTest(APITestCase):
    def setUp(self):
        # Create a test product
        self.product = Product.objects.create(
            title="Test Product",
            description="Test Description",
            price=100.00,
        )

        # Create a test user
        self.user = CustomUser.objects.create_customer(
            username="test_user",
            password="password123",
            first_name="John",
            last_name="Doe",
        )

        # Create a test blog
        self.blog = Blog.objects.create(
            title="Test Blog",
            description="Test Description",
            product=self.product,
            content_file=SimpleUploadedFile(
                "test_file.txt", b"file_content", content_type="text/plain"
            ),
        )

        # Create a test comment
        self.comment = Comment.objects.create(
            user=self.user,
            content="Test Comment",
            blog=self.blog,
        )

        # Create a test card
        self.card = Card.objects.create(user=self.user)

        # Create a test order card
        self.order_card = OrderCard.objects.create(
            card=self.card,
            product=self.product,
            order_time=2,
        )

    # ----------------------
    # BlogFullSerializer Tests
    # ----------------------

    def test_blog_full_serializer(self):
        """Test if BlogFullSerializer returns all fields correctly"""
        serializer = BlogFullSerializer(self.blog)
        data = serializer.data

        # Check if all fields are present
        self.assertIn("id", data)
        self.assertIn("title", data)
        self.assertIn("description", data)
        self.assertIn("product", data)
        self.assertIn("content_file", data)
        self.assertIn("active", data)

        # Check if the data is correct
        self.assertEqual(data["title"], "Test Blog")
        self.assertEqual(data["description"], "Test Description")
        self.assertEqual(data["product"], self.product.id)
        self.assertTrue(data["content_file"].startswith("/media/blog_content/"))
        self.assertEqual(data["active"], True)

    # ----------------------
    # BlogSerializerShow Tests
    # ----------------------

    def test_blog_serializer_show(self):
        """Test if BlogSerializerShow returns only selected fields"""
        serializer = BlogSerializerShow(self.blog)
        data = serializer.data

        # Check if only selected fields are present
        self.assertEqual(list(data.keys()), ["title", "description"])

        # Check if the data is correct
        self.assertEqual(data["title"], "Test Blog")
        self.assertEqual(data["description"], "Test Description")

    # ----------------------
    # CommentSerializer Tests
    # ----------------------

    def test_comment_serializer(self):
        """Test if CommentSerializer returns all fields correctly"""
        serializer = CommentSerializer(self.comment)
        data = serializer.data

        # Check if all fields are present
        self.assertIn("id", data)
        self.assertIn("user", data)
        self.assertIn("content", data)
        self.assertIn("blog", data)

        # Check if the data is correct
        self.assertEqual(data["user"], self.user.id)
        self.assertEqual(data["content"], "Test Comment")
        self.assertEqual(data["blog"], self.blog.id)

    # ----------------------
    # CardSerializer Tests
    # ----------------------

    def test_card_serializer(self):
        """Test if CardSerializer returns all fields correctly"""
        serializer = CardSerializer(self.card)
        data = serializer.data

        # Check if all fields are present
        self.assertIn("id", data)
        self.assertIn("user", data)

        # Check if the data is correct
        self.assertEqual(data["user"], self.user.id)

    # ----------------------
    # OrderCardSerializer Tests
    # ----------------------

    def test_order_card_serializer(self):
        """Test if OrderCardSerializer returns all fields correctly"""
        serializer = OrderCardSerializer(self.order_card)
        data = serializer.data

        # Check if all fields are present
        self.assertIn("id", data)
        self.assertIn("card", data)
        self.assertIn("product", data)
        self.assertIn("order_time", data)

        # Check if the data is correct
        self.assertEqual(data["card"], self.card.id)
        self.assertEqual(data["product"], self.product.id)
        self.assertEqual(data["order_time"], 2)

    def tearDown(self):
        # Clean up uploaded files
        if self.blog.content_file:
            self.blog.content_file.delete()
