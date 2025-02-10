from django.db import models


# Model representing an industry category
class Industry(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


# Model representing product colors
class ProductColor(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


# Model representing a product
class Product(models.Model):
    industry = models.ForeignKey(
        "Industry",
        on_delete=models.CASCADE,
        null=True,
        blank=True,  # Links product to an industry
    )
    title = models.CharField(max_length=150)  # Product title
    descriptions = models.TextField()  # Product description
    length = models.IntegerField(null=True, blank=True)  # Product length (optional)
    width = models.IntegerField(null=True, blank=True)  # Product width (optional)
    weight = models.IntegerField(null=True, blank=True)  # Product weight (optional)
    color = models.ForeignKey(
        "ProductColor",
        on_delete=models.CASCADE,
        null=True,
        blank=True,  # Links product to a color
    )

    def __str__(self):
        return self.title
