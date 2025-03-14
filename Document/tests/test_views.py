from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from models import Blog, Comment, Card, OrderCard
from Product.models import Product
from AuthenticationSystem.models import CustomUser
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.cache import cache


class ViewsTest(TestCase):
    def setUp(self):
        # Create a test client
        self.client = APIClient()

        # Create a test product
        self.product = Product.objects.create(
            title="Test Product",
            description="Test Description",
            price=100.00,
        )

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
            user=self.customer,
            content="Test Comment",
            blog=self.blog,
        )

        # Create a test card
        self.card = Card.objects.create(user=self.customer)

        # Create a test order card
        self.order_card = OrderCard.objects.create(
            card=self.card,
            product=self.product,
            order_time=2,
        )

        # Generate tokens for the test users
        self.customer_tokens = self.get_tokens_for_user(self.customer)
        self.store_owner_tokens = self.get_tokens_for_user(self.store_owner)

    def get_tokens_for_user(self, user):
        """Helper function to generate JWT tokens for a user"""
        from rest_framework_simplejwt.tokens import RefreshToken

        refresh = RefreshToken.for_user(user)
        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }

    # ----------------------
    # Create Blog View Tests
    # ----------------------

    def test_create_blog_success(self):
        """Test creating a blog post with valid data"""
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.store_owner_tokens['access']}"
        )
        url = reverse("create_blog")
        data = {
            "product_id": self.product.id,
            "title": "New Blog",
            "description": "New Description",
            "content_file": SimpleUploadedFile(
                "test_file.html", b"<p>Test Content</p>", content_type="text/html"
            ),
        }
        response = self.client.post(url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response.data)

    def test_create_blog_invalid_user(self):
        """Test creating a blog post with a non-store owner user"""
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.customer_tokens['access']}"
        )
        url = reverse("create_blog")
        data = {
            "product_id": self.product.id,
            "title": "New Blog",
            "description": "New Description",
            "content_file": SimpleUploadedFile(
                "test_file.html", b"<p>Test Content</p>", content_type="text/html"
            ),
        }
        response = self.client.post(url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # ----------------------
    # Delete Blog View Tests
    # ----------------------

    def test_delete_blog_success(self):
        """Test deleting a blog post with valid data"""
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.store_owner_tokens['access']}"
        )
        url = reverse("delete_blog")
        data = {"blog_id": self.blog.id}
        response = self.client.delete(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_blog_invalid_user(self):
        """Test deleting a blog post with a non-store owner user"""
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.customer_tokens['access']}"
        )
        url = reverse("delete_blog")
        data = {"blog_id": self.blog.id}
        response = self.client.delete(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # ----------------------
    # Get Cart View Tests
    # ----------------------

    def test_get_cart_success(self):
        """Test retrieving the user's cart"""
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.customer_tokens['access']}"
        )
        url = reverse("get_cart")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("cart", response.data)

    def test_get_cart_not_found(self):
        """Test retrieving a non-existent cart"""
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.store_owner_tokens['access']}"
        )
        url = reverse("get_cart")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # ----------------------
    # Update Blog View Tests
    # ----------------------

    def test_update_blog_success(self):
        """Test updating a blog post with valid data"""
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.store_owner_tokens['access']}"
        )
        url = reverse("update_blog")
        data = {
            "product_id": self.product.id,
            "title": "Updated Blog",
            "description": "Updated Description",
            "content_file": SimpleUploadedFile(
                "test_file.html", b"<p>Updated Content</p>", content_type="text/html"
            ),
        }
        response = self.client.put(url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_blog_invalid_user(self):
        """Test updating a blog post with a non-store owner user"""
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.customer_tokens['access']}"
        )
        url = reverse("update_blog")
        data = {
            "product_id": self.product.id,
            "title": "Updated Blog",
            "description": "Updated Description",
            "content_file": SimpleUploadedFile(
                "test_file.html", b"<p>Updated Content</p>", content_type="text/html"
            ),
        }
        response = self.client.put(url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # ----------------------
    # Blog Dependent on Product View Tests
    # ----------------------

    def test_blog_dependent_on_product_success(self):
        """Test retrieving blogs dependent on a product"""
        url = reverse("blog_dependent_on_product")
        response = self.client.get(url, {"product_id": self.product.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("product_blogs", response.data)

    def test_blog_dependent_on_product_not_found(self):
        """Test retrieving blogs for a non-existent product"""
        url = reverse("blog_dependent_on_product")
        response = self.client.get(url, {"product_id": 999})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # ----------------------
    # Show All Blogs View Tests
    # ----------------------

    def test_show_all_blogs_success(self):
        """Test retrieving all active blogs"""
        url = reverse("show_all_blogs")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("blogs_list", response.data)

    # ----------------------
    # Show Comments Dependent on Blog View Tests
    # ----------------------

    def test_show_comments_dependent_on_blog_success(self):
        """Test retrieving comments dependent on a blog"""
        url = reverse("show_comments_dependent_on_blog")
        response = self.client.get(url, {"blog_id": self.blog.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("comments", response.data)

    def test_show_comments_dependent_on_blog_not_found(self):
        """Test retrieving comments for a non-existent blog"""
        url = reverse("show_comments_dependent_on_blog")
        response = self.client.get(url, {"blog_id": 999})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # ----------------------
    # Create Comment View Tests
    # ----------------------

    def test_create_comment_success(self):
        """Test creating a comment with valid data"""
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.customer_tokens['access']}"
        )
        url = reverse("create_comment")
        data = {
            "blog_id": self.blog.id,
            "content": "New Comment",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_comment_invalid_blog(self):
        """Test creating a comment for a non-existent blog"""
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.customer_tokens['access']}"
        )
        url = reverse("create_comment")
        data = {
            "blog_id": 999,
            "content": "New Comment",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # ----------------------
    # Delete Comment View Tests
    # ----------------------

    def test_delete_comment_success(self):
        """Test deleting a comment with valid data"""
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.customer_tokens['access']}"
        )
        url = reverse("delete_comment")
        data = {
            "blog_id": self.blog.id,
        }
        response = self.client.delete(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_comment_invalid_user(self):
        """Test deleting a comment with a non-owner user"""
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.store_owner_tokens['access']}"
        )
        url = reverse("delete_comment")
        data = {
            "blog_id": self.blog.id,
        }
        response = self.client.delete(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # ----------------------
    # Add Product to Cart View Tests
    # ----------------------

    def test_add_product_to_cart_success(self):
        """Test adding a product to the cart with valid data"""
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.customer_tokens['access']}"
        )
        url = reverse("add_product_to_cart")
        data = {
            "product_id": self.product.id,
            "order_time": 1,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_product_to_cart_invalid_product(self):
        """Test adding a non-existent product to the cart"""
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.customer_tokens['access']}"
        )
        url = reverse("add_product_to_cart")
        data = {
            "product_id": 999,
            "order_time": 1,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # ----------------------
    # Remove Product from Cart View Tests
    # ----------------------

    def test_remove_product_from_cart_success(self):
        """Test removing a product from the cart with valid data"""
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.customer_tokens['access']}"
        )
        url = reverse("remove_product_from_cart")
        data = {
            "product_id": self.product.id,
        }
        response = self.client.delete(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_remove_product_from_cart_invalid_product(self):
        """Test removing a non-existent product from the cart"""
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.customer_tokens['access']}"
        )
        url = reverse("remove_product_from_cart")
        data = {
            "product_id": 999,
        }
        response = self.client.delete(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def tearDown(self):
        # Clean up uploaded files
        if self.blog.content_file:
            self.blog.content_file.delete()
        # Clear cache
        cache.clear()
