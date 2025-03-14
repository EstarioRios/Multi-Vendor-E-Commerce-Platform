from django.test import TestCase
from Product.models import Product
from AuthenticationSystem.models import CustomUser
from models import Blog, Comment, Card, OrderCard
from django.core.files.uploadedfile import SimpleUploadedFile


class ModelsTest(TestCase):
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
    # Blog Model Tests
    # ----------------------

    def test_blog_creation(self):
        """Test if a blog is created correctly"""
        self.assertEqual(self.blog.title, "Test Blog")
        self.assertEqual(self.blog.description, "Test Description")
        self.assertEqual(self.blog.product, self.product)
        self.assertTrue(self.blog.content_file.name.startswith("blog_content/"))
        self.assertTrue(self.blog.active)

    def test_blog_str_method(self):
        """Test the __str__ method of the Blog model"""
        self.assertEqual(str(self.blog), "Test Blog for Test Product")

    # ----------------------
    # Comment Model Tests
    # ----------------------

    def test_comment_creation(self):
        """Test if a comment is created correctly"""
        self.assertEqual(self.comment.user, self.user)
        self.assertEqual(self.comment.content, "Test Comment")
        self.assertEqual(self.comment.blog, self.blog)

    def test_comment_str_method(self):
        """Test the __str__ method of the Comment model"""
        self.assertEqual(str(self.comment), "Comment on Test Blog")

    # ----------------------
    # Card Model Tests
    # ----------------------

    def test_card_creation(self):
        """Test if a card is created correctly"""
        self.assertEqual(self.card.user, self.user)

    def test_card_str_method(self):
        """Test the __str__ method of the Card model"""
        self.assertEqual(str(self.card), "John Doe's cart")

    # ----------------------
    # OrderCard Model Tests
    # ----------------------

    def test_order_card_creation(self):
        """Test if an order card is created correctly"""
        self.assertEqual(self.order_card.card, self.card)
        self.assertEqual(self.order_card.product, self.product)
        self.assertEqual(self.order_card.order_time, 2)

    def test_order_card_str_method(self):
        """Test the __str__ method of the OrderCard model"""
        self.assertEqual(str(self.order_card), "2x Test Product in test_user's cart")

    def test_order_card_unique_together(self):
        """Test the unique_together constraint of the OrderCard model"""
        with self.assertRaises(Exception):
            OrderCard.objects.create(
                card=self.card,
                product=self.product,
                order_time=3,
            )

    def tearDown(self):
        # Clean up uploaded files
        if self.blog.content_file:
            self.blog.content_file.delete()
