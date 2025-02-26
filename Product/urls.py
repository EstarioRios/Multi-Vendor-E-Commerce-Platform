from django.urls import path
from .views import (
    industries_list_show,
    products_sort_show,
    product_detail,
    create_product,
    show_products_by_store,
    delete_product,
)

urlpatterns = [
    # Retrieve all industries
    path("industries/", industries_list_show, name="industries-list"),
    # Retrieve sorted products based on filters
    path("products/sort/", products_sort_show, name="products-sort"),
    # Retrieve details of a specific product
    path("product/detail/", product_detail, name="product-detail"),
    # Create a new product (store owners only)
    path("product/create/", create_product, name="create-product"),
    # Retrieve all products of a specific store owner
    path("products/store/", show_products_by_store, name="store-products"),
    # Delete a product (only for store owners or admins)
    path("product/delete/", delete_product, name="delete-product"),
]
