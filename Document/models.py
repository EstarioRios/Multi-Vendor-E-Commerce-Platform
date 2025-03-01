from django.db import models
from Product.models import Product
from AuthenticationSystem.models import CustomUser


# Blog model to store blog posts related to a product
class Blog(models.Model):
    title = models.CharField(max_length=100)  # Blog title
    description = models.TextField()  # Short description of the blog
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="blogs"
    )  # Related product
    content_file = models.FileField(upload_to="blog_content/")  # File for blog content

    def __str__(self):
        return f"{self.title} for {self.product.title}"


# Comment model to store comments on blog posts
class Comment(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="comments"
    )  # User who wrote the comment
    content = models.TextField()  # Comment text
    blog = models.ForeignKey(
        Blog, on_delete=models.CASCADE, related_name="comments"
    )  # Related blog post

    def __str__(self):
        return f"Comment on {self.blog.title}"


class Card(models.Model):
    """
    Model representing a shopping cart for a user.
    Each user has only one cart.
    """

    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="card",  # Access the user's cart using user.card
        verbose_name="User",  # Human-readable name for admin
    )

    def __str__(self):
        """
        String representation of the Cart model.
        """
        return f"{self.user.first_name} {self.user.last_name}'s cart"

    class Meta:
        verbose_name = "Cart"  # Singular name for admin
        verbose_name_plural = "Carts"  # Plural name for admin


class OrderCard(models.Model):
    """
    Model representing an item in a shopping cart.
    Each item is associated with a cart and a product.
    """

    card = models.ForeignKey(
        Card,
        on_delete=models.CASCADE,
        related_name="orders",  # Access all orders in a cart using card.orders
        verbose_name="Cart",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="orders",  # Access all orders for a product using product.orders
        verbose_name="Product",
    )
    order_time = models.PositiveIntegerField(
        default=1, verbose_name="Quantity"  # Default quantity is 1
    )

    def __str__(self):
        """
        String representation of the OrderCard model.
        """
        return f"{self.order_time}x {self.product.title} in {self.card.user.username}'s cart"

    class Meta:
        verbose_name = "Order Item"  # Singular name for admin
        verbose_name_plural = "Order Items"  # Plural name for admin
        unique_together = (
            "card",
            "product",
        )  # Ensures a product can only be added once per cart
