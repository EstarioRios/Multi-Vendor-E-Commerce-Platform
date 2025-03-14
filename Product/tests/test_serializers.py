from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from rest_framework import status
from models import Product, Industry, MainImage, ProductImage, ProductColor, TypeOfFile
from serializers import (
    MainImageSerializer,
    ProductImageSerializer,
    ProductSerializerFull,
    ProductSerializerShow,
    IndustrySerializer,
)


class SerializersTest(TestCase):
    def setUp(self):
        """
        Set up initial data for testing serializers.
        """
        # Create an Industry instance
        self.industry = Industry.objects.create(name="Technology")

        # Create a ProductColor instance
        self.color = ProductColor.objects.create(name="Blue")

        # Create a TypeOfFile instance
        self.file_type = TypeOfFile.objects.create(name_of_type="PDF")

        # Create a Product instance
        self.product = Product.objects.create(
            title="Smartphone",
            descriptions="A high-end smartphone",
            price=1000.00,
            product_type="Physical",
            industry=self.industry,
            color=self.color,
        )

        # Create a ProductImage instance
        self.image = SimpleUploadedFile(
            "test_image.jpg", b"file_content", content_type="image/jpeg"
        )
        self.product_image = ProductImage.objects.create(
            product=self.product, image=self.image
        )

        # Create a MainImage instance
        self.main_image = MainImage.objects.create(
            product=self.product, product_image=self.product_image
        )

    def test_main_image_serializer(self):
        """
        Test the MainImageSerializer to ensure it serializes the MainImage model correctly.
        """
        serializer = MainImageSerializer(instance=self.main_image)
        self.assertEqual(serializer.data["product_image"], self.product_image.image.url)

    def test_product_image_serializer(self):
        """
        Test the ProductImageSerializer to ensure it serializes the ProductImage model correctly.
        """
        serializer = ProductImageSerializer(instance=self.product_image)
        self.assertEqual(serializer.data["image"], self.product_image.image.url)

    def test_product_serializer_full(self):
        """
        Test the ProductSerializerFull to ensure it serializes all fields of the Product model correctly.
        """
        serializer = ProductSerializerFull(instance=self.product)
        self.assertEqual(serializer.data["title"], self.product.title)
        self.assertEqual(serializer.data["descriptions"], self.product.descriptions)
        self.assertEqual(serializer.data["price"], str(self.product.price))
        self.assertEqual(serializer.data["product_type"], self.product.product_type)
        self.assertEqual(serializer.data["industry"], self.industry.id)
        self.assertEqual(serializer.data["color"], self.color.id)

    def test_product_serializer_show(self):
        """
        Test the ProductSerializerShow to ensure it serializes selected fields of the Product model correctly.
        """
        serializer = ProductSerializerShow(instance=self.product)
        self.assertEqual(serializer.data["title"], self.product.title)
        self.assertEqual(serializer.data["descriptions"], self.product.descriptions)
        self.assertEqual(serializer.data["price"], str(self.product.price))
        self.assertEqual(serializer.data["product_type"], self.product.product_type)
        self.assertEqual(serializer.data["industry"], self.industry.id)
        self.assertEqual(
            serializer.data["main_image"], self.main_image.product_image.image.url
        )

    def test_industry_serializer(self):
        """
        Test the IndustrySerializer to ensure it serializes the Industry model correctly.
        """
        serializer = IndustrySerializer(instance=self.industry)
        self.assertEqual(serializer.data["name"], self.industry.name)
