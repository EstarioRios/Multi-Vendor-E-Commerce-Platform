from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from models import Industry, ProductColor, TypeOfFile, Product, ProductImage, MainImage


class IndustryModelTest(TestCase):
    def test_industry_creation(self):
        """
        Test the creation of an Industry instance and its string representation.
        """
        industry = Industry.objects.create(name="Technology")
        self.assertEqual(industry.name, "Technology")
        self.assertEqual(str(industry), "Technology")


class ProductColorModelTest(TestCase):
    def test_product_color_creation(self):
        """
        Test the creation of a ProductColor instance and its string representation.
        """
        color = ProductColor.objects.create(name="Red")
        self.assertEqual(color.name, "Red")
        self.assertEqual(str(color), "Red")


class TypeOfFileModelTest(TestCase):
    def test_type_of_file_creation(self):
        """
        Test the creation of a TypeOfFile instance and its string representation.
        """
        file_type = TypeOfFile.objects.create(name_of_type="PDF")
        self.assertEqual(file_type.name_of_type, "PDF")
        self.assertEqual(str(file_type), "PDF")


class ProductModelTest(TestCase):
    def setUp(self):
        """
        Set up initial data for Product-related tests.
        """
        self.industry = Industry.objects.create(name="Technology")
        self.color = ProductColor.objects.create(name="Blue")
        self.file_type = TypeOfFile.objects.create(name_of_type="ZIP")

    def test_physical_product_creation(self):
        """
        Test the creation of a Physical Product and validate its attributes.
        """
        product = Product.create_physical(
            title="Laptop",
            description="A high-end gaming laptop",
            length=30,
            width=20,
            color=self.color,
            weight=2,
            price=1500.00,
        )
        self.assertEqual(product.title, "Laptop")
        self.assertEqual(product.product_type, "Physical")
        self.assertEqual(product.length, 30)
        self.assertEqual(product.width, 20)
        self.assertEqual(product.color.name, "Blue")
        self.assertEqual(product.weight, 2)
        self.assertEqual(product.price, 1500.00)

    def test_digital_product_creation(self):
        """
        Test the creation of a Digital Product and validate its attributes.
        """
        product = Product.create_digital(
            title="Ebook",
            description="A guide to Django",
            size=5,
            type_of_file=self.file_type,
            price=20.00,
        )
        self.assertEqual(product.title, "Ebook")
        self.assertEqual(product.product_type, "Digital")
        self.assertEqual(product.size, 5)
        self.assertEqual(product.type_of_file.name_of_type, "ZIP")
        self.assertEqual(product.price, 20.00)


class ProductImageModelTest(TestCase):
    def setUp(self):
        """
        Set up initial data for ProductImage-related tests.
        """
        self.industry = Industry.objects.create(name="Technology")
        self.product = Product.objects.create(
            title="Smartphone",
            descriptions="A high-end smartphone",
            price=1000.00,
            product_type="Physical",
            industry=self.industry,
        )

    def test_product_image_creation(self):
        """
        Test the creation of a ProductImage instance and its string representation.
        """
        image = SimpleUploadedFile(
            "test_image.jpg", b"file_content", content_type="image/jpeg"
        )
        product_image = ProductImage.objects.create(product=self.product, image=image)
        self.assertEqual(str(product_image), f"Image for {self.product.title}")


class MainImageModelTest(TestCase):
    def setUp(self):
        """
        Set up initial data for MainImage-related tests.
        """
        self.industry = Industry.objects.create(name="Technology")
        self.product = Product.objects.create(
            title="Smartphone",
            descriptions="A high-end smartphone",
            price=1000.00,
            product_type="Physical",
            industry=self.industry,
        )
        self.image = SimpleUploadedFile(
            "test_image.jpg", b"file_content", content_type="image/jpeg"
        )
        self.product_image = ProductImage.objects.create(
            product=self.product, image=self.image
        )

    def test_main_image_creation(self):
        """
        Test the creation of a MainImage instance and its string representation.
        """
        main_image = MainImage.objects.create(
            product=self.product, product_image=self.product_image
        )
        self.assertEqual(str(main_image), f"Main image for {self.product.title}")
