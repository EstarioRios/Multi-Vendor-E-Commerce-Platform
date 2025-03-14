from django.test import TestCase, RequestFactory
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient, force_authenticate
from rest_framework import status
from django.core.cache import cache
from uuid import UUID
from models import Product, Industry, ProductColor, TypeOfFile, ProductImage, MainImage
from AuthenticationSystem.models import CustomUser
from views import (
    industries_list_show,
    products_sort_show,
    product_detail,
    create_product,
    show_products_by_store,
    delete_product,
)
from serializers import (
    ProductSerializerShow,
    IndustrySerializer,
    ProductSerializerFull,
)


class ViewsTest(TestCase):
    def setUp(self):
        """
        Set up initial data for testing views.
        """
        self.client = APIClient()
        self.factory = RequestFactory()

        # Create an Industry instance
        self.industry = Industry.objects.create(name="Technology")

        # Create a ProductColor instance
        self.color = ProductColor.objects.create(name="Blue")

        # Create a TypeOfFile instance
        self.file_type = TypeOfFile.objects.create(name_of_type="PDF")

        # Create a CustomUser instance (store owner)
        self.store_owner = CustomUser.objects.create(
            username="store_owner",
            email="store_owner@example.com",
            user_type="store_owner",
        )

        # Create a Product instance
        self.product = Product.objects.create(
            title="Smartphone",
            descriptions="A high-end smartphone",
            price=1000.00,
            product_type="Physical",
            industry=self.industry,
            color=self.color,
            store_owner=self.store_owner,
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

        # Clear cache before each test
        cache.clear()

    def test_industries_list_show(self):
        """
        Test the industries_list_show view to ensure it returns the correct list of industries.
        """
        request = self.factory.get("/industries/")
        response = industries_list_show(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["industries"]), 1)

    def test_products_sort_show(self):
        """
        Test the products_sort_show view to ensure it filters products correctly.
        """
        # Test filtering by product_type and industry
        request = self.factory.get(
            "/products/sort/?product_type=Physical&industry={self.industry.id}"
        )
        response = products_sort_show(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["products"]), 1)

        # Test filtering by product_type, industry, and title
        request = self.factory.get(
            f"/products/sort/?product_type=Physical&industry={self.industry.id}&title=Smartphone"
        )
        response = products_sort_show(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["products"]), 1)

        # Test invalid product_type
        request = self.factory.get(
            f"/products/sort/?product_type=Invalid&industry={self.industry.id}"
        )
        response = products_sort_show(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_product_detail(self):
        """
        Test the product_detail view to ensure it returns the correct product details.
        """
        request = self.factory.get(f"/product/detail/?product_id={self.product.id}")
        response = product_detail(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["product_detail"]["title"], self.product.title)

        # Test invalid product_id
        request = self.factory.get("/product/detail/?product_id=invalid")
        response = product_detail(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_product(self):
        """
        Test the create_product view to ensure it creates a product correctly.
        """
        # Authenticate the store owner
        self.client.force_authenticate(user=self.store_owner)

        # Create a physical product
        data = {
            "product_title": "Laptop",
            "product_price": "1500.00",
            "description": "A high-end gaming laptop",
            "product_type": "Physical",
            "length": 30,
            "width": 20,
            "color": "Blue",
        }
        images = [
            SimpleUploadedFile(
                "test_image.jpg", b"file_content", content_type="image/jpeg"
            )
        ]
        response = self.client.post(
            "/create-product/", data=data, files={"images": images}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "Laptop")

        # Create a digital product
        data = {
            "product_title": "Ebook",
            "product_price": "20.00",
            "description": "A guide to Django",
            "product_type": "Digital",
            "size": 5,
            "type_of_file": "PDF",
        }
        response = self.client.post(
            "/create-product/", data=data, files={"images": images}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "Ebook")

        # Test invalid product type
        data = {
            "product_title": "Invalid Product",
            "product_price": "100.00",
            "product_type": "Invalid",
        }
        response = self.client.post("/create-product/", data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_show_products_by_store(self):
        """
        Test the show_products_by_store view to ensure it returns the correct list of products for a store owner.
        """
        request = self.factory.get(
            f"/store/products/?store_owner_id={self.store_owner.id}"
        )
        response = show_products_by_store(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["products"]), 1)

        # Test invalid store_owner_id
        request = self.factory.get("/store/products/?store_owner_id=invalid")
        response = show_products_by_store(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_product(self):
        """
        Test the delete_product view to ensure it deletes a product correctly.
        """
        # Authenticate the store owner
        self.client.force_authenticate(user=self.store_owner)

        # Delete the product
        response = self.client.delete(f"/delete-product/?product_id={self.product.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Test invalid product_id
        response = self.client.delete("/delete-product/?product_id=invalid")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
