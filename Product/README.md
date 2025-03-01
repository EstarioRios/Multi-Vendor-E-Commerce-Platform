# Product Management Module

## Overview
The Product Management module is designed to handle the creation, organization, and retrieval of products in a multi-vendor platform. It supports both physical and digital products, allowing store owners to manage their inventory effectively. The module integrates with the Authentication System to ensure that only authorized users can create or modify products.

---

## Key Features
1. **Product Types**:
   - **Physical Products**: Products with physical attributes like length, width, weight, and color.
   - **Digital Products**: Products with digital attributes like file size and file type.

2. **Product Attributes**:
   - Common fields: Title, price, description, industry, and active status.
   - Physical-specific fields: Length, width, weight, and color.
   - Digital-specific fields: File size and file type.

3. **Product Images**:
   - Supports multiple images per product.
   - Allows setting a main image for each product.

4. **Industry and File Type Management**:
   - Products are categorized by industry.
   - Digital products are classified by file type (e.g., PDF, ZIP).

---

## How It Works
The Product Management module is built using Django and Django REST Framework. It provides endpoints for creating, retrieving, and deleting products. The module ensures that only store owners can create or modify products, while customers can browse and view product details.

### Key Components
1. **Product Model**:
   - Handles both physical and digital products.
   - Includes methods for creating physical and digital products.

2. **ProductImage Model**:
   - Manages multiple images for each product.
   - Supports setting a main image.

3. **Industry and File Type Models**:
   - Categorizes products by industry and file type.

4. **API Endpoints**:
   - Provides endpoints for retrieving product details, filtering products, and managing product creation/deletion.

---

## API Documentation

### 1. Retrieve All Industries
- **Endpoint**: `GET /product/industries/`
- **Response**:
  - List of all industries with their IDs and names.

### 2. Retrieve Sorted Products
- **Endpoint**: `GET /product/products/sort/`
- **Parameters**:
  - `product_type`: Type of product (Physical/Digital).
  - `industry`: ID of the industry.
  - `title`: Optional. Filters products by title.
  - `type_of_file`: Required for digital products. Filters by file type.
- **Response**:
  - List of products matching the filters.

### 3. Retrieve Product Details
- **Endpoint**: `GET /product/product/detail/`
- **Parameters**:
  - `product_id`: ID of the product.
- **Response**:
  - Detailed information about the product, including images.

### 4. Create a Product
- **Endpoint**: `POST /product/product/create/`
- **Headers**:
  - `Authorization`: Bearer <access_token>
- **Parameters**:
  - `product_title`: Title of the product.
  - `product_price`: Price of the product.
  - `description`: Description of the product.
  - `product_type`: Type of product (Physical/Digital).
  - For physical products: `length`, `width`, `color`.
  - For digital products: `size`, `type_of_file`.
  - `images`: At least one image file (required).
- **Response**:
  - Detailed information about the created product.

### 5. Retrieve Products by Store
- **Endpoint**: `GET /product/products/store/`
- **Parameters**:
  - `store_owner_id`: ID of the store owner.
- **Response**:
  - List of products associated with the store owner.

### 6. Delete a Product
- **Endpoint**: `DELETE /product/product/delete/`
- **Headers**:
  - `Authorization`: Bearer <access_token>
- **Parameters**:
  - `product_id`: ID of the product to delete.
- **Response**:
  - Confirmation of product deletion.

