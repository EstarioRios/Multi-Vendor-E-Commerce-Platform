from django.db import models


# Model representing an industry category
class Industry(models.Model):
    name = models.CharField(max_length=50)  # Industry name

    def __str__(self):
        return self.name


# Model representing product colors
class ProductColor(models.Model):
    name = models.CharField(max_length=50)  # Color name

    def __str__(self):
        return self.name


# Model for product file types (used for digital products)
class TypeOfFile(models.Model):
    name_of_type = models.CharField(
        max_length=12
    )  # Name of the file type (e.g., PDF, ZIP)

    def __str__(self):
        return self.name_of_type


# Model representing a product
class Product(models.Model):

    # Fields that are common to both physical and digital products
    industry = models.ForeignKey(
        "Industry",
        on_delete=models.CASCADE,
        null=True,
        blank=True,  # Links product to an industry (optional)
    )
    title = models.CharField(max_length=150)  # Product title
    descriptions = models.TextField()  # Product description
    product_type = models.CharField(
        max_length=10,
        choices=[("Physical", "Physical"), ("Digital", "Digital")],
        default="Physical",
    )  # Type of the product (Physical or Digital)
    created_at = models.DateTimeField(
        auto_now_add=True
    )  # Timestamp of when the product was created

    # Fields specific to physical products
    length = models.IntegerField(null=True, blank=True)  # Product length (optional)
    width = models.IntegerField(null=True, blank=True)  # Product width (optional)
    weight = models.IntegerField(null=True, blank=True)  # Product weight (optional)
    color = models.ForeignKey(
        "ProductColor",
        on_delete=models.CASCADE,
        null=True,
        blank=True,  # Links product to a color (optional)
    )

    # Fields specific to digital products
    size = models.IntegerField(
        null=True, blank=True
    )  # File size for digital products (optional)
    type_of_file = models.ForeignKey(
        "TypeOfFile", on_delete=models.CASCADE, null=True, blank=True
    )  # Type of file (e.g., PDF, ZIP) for digital products

    def create_physical(self, title, description, length, width, color, weight):
        """
        Method to create a physical product
        Accepts parameters to define physical product attributes
        """
        if self.product_type == "Physical":
            self.title = title
            self.descriptions = description
            self.product_type = "Physical"  # Sets the product type to Physical
            self.length = length
            self.width = width
            self.color = color
            self.weight = weight
            type_of_file = None
            size = None
            self.save()  # Saves the product to the database

    def create_digital(self, title, description, size, type_of_file):
        """
        Method to create a digital product
        Accepts parameters to define digital product attributes
        """
        if self.product_type == "Digital":
            self.title = title
            self.descriptions = description
            self.product_type = "Digital"  # Sets the product type to Digital
            self.size = size
            self.type_of_file = type_of_file
            self.save()  # Saves the product to the database

    def __str__(self):
        return self.title  # Returns the product title when the object is printed
