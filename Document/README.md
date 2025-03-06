# E-Commerce Core Module

## Overview
The E-Commerce Core module handles blog management, comment systems, and shopping cart functionality for a multi-vendor platform. Built with Django REST Framework, it integrates with JWT authentication and supports role-based access control.

---

## Key Features
1. **Blog Management**:
   - Create/update/delete product-related blogs.
   - HTML content sanitization and validation.
   - Active/inactive status control for blogs.

2. **Comment System**:
   - User comments on blog posts.
   - Comment deletion by owners/admins.
   - Blog-specific comment retrieval.

3. **Shopping Cart**:
   - Add/remove products with quantity management.
   - Unique product enforcement per cart.
   - Cart persistence per user.

4. **Security**:
   - JWT-based authentication.
   - Role-based permissions (Customers/Store Owners/Admins).
   - HTML file validation (MIME type and content sanitization).

---

## How It Works
The module uses Django models and REST Framework API endpoints to handle e-commerce operations. It integrates with the authentication system for user validation and permission checks.

### Key Components
1. **Core Models**:
   - `Blog`: Stores blog posts with product relationships
   - `Comment`: Manages user comments on blogs
   - `Card`: Represents user shopping carts
   - `OrderCard`: Tracks product quantities in carts

2. **Workflow**:
   - Store owners create blogs via `/document/blogs/create/` with HTML content
   - Users interact with blogs through comments (`/comments/` endpoints)
   - Cart operations use `/cart/` endpoints with JWT validation
   - Admin users can moderate content through delete endpoints

3. **URL Configuration**:
   - All endpoints are defined in `core/urls.py`
   - Integrated with project-level routing

---

## API Documentation

### 1. Blog Management
- **Create Blog**:  
  `POST /document/blogs/create/`  
  **Headers**:  
  `Authorization: Bearer <access_token>`  
  **Parameters**:
  - `product_id` (required)
  - `title` (required)
  - `description` (required)
  - `content_file` (HTML file - required)  
  **Access**: Store Owners only

- **Delete Blog**:  
  `DELETE /document/blogs/delete/`  
  **Headers**:  
  `Authorization: Bearer <access_token>`  
  **Parameters**:
  - `blog_id` (query parameter)  
  **Access**: Store Owners/Admins

- **Get Product Blogs**:  
  `GET /document/blogs/by-product/?product_id=<id>`  