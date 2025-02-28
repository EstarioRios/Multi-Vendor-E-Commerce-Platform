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
