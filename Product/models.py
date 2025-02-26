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
    price = models.DecimalField(
        decimal_places=2, default=0, max_digits=10
    )  # Product price
    active = models.BooleanField(default=True)
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
    store_owner = models.ForeignKey(
        "AuthenticationSystem.CustomUser",
        on_delete=models.CASCADE,
        related_name="products",
    )

    @classmethod
    def create_physical(cls, title, description, length, width, color, weight, price):
        """
        Class method to create a physical product
        """
        return cls.objects.create(
            title=title,
            price=price,
            descriptions=description,
            product_type="Physical",
            length=length,
            width=width,
            color=color,
            weight=weight,
            size=None,
            type_of_file=None,
        )

    @classmethod
    def create_digital(cls, title, description, size, type_of_file, price):
        """
        Class method to create a digital product
        """
        return cls.objects.create(
            title=title,
            price=price,
            descriptions=description,
            product_type="Digital",
            size=size,
            type_of_file=type_of_file,
            length=None,
            width=None,
            color=None,
            weight=None,
        )
        """
        Method to create a digital product
        Accepts parameters to define digital product attributes
        """

        self.title = title
        self.price = price
        self.descriptions = description
        self.product_type = "Digital"  # Sets the product type to Digital
        self.size = size
        self.type_of_file = type_of_file
        self.save()  # Saves the product to the database

    def __str__(self):
        return self.title  # Returns the product title when the object is printed


# Model for storing images associated with a product
class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )  # Links product to its images (one-to-many relationship)
    image = models.ImageField(
        upload_to="product_images/"
    )  # Stores the image file in the product_images folder
    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )  # Records the date and time when the image was uploaded

    def __str__(self):
        return f"Image for {self.product.title}"  # String representation of the image


# Model for setting the main image for a product
class MainImage(models.Model):
    product = models.OneToOneField(
        Product, on_delete=models.CASCADE, related_name="main_image"
    )  # Links a single product to its main image (one-to-one relationship)
    product_image = models.ForeignKey(
        ProductImage, on_delete=models.CASCADE, related_name="main_for"
    )  # Links to the ProductImage that is designated as the main image

    def __str__(self):
        return f"Main image for {self.product.title}"  # String representation of the main image
