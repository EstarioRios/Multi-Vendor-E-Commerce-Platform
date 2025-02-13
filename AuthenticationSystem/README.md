# Authentication System

## Overview
This system provides authentication and user management functionalities using Django REST Framework and JWT authentication.

## User Roles & Permissions
### 1. WebOwner
- **Role:** Website owner
- **Permissions:**
  - Manage Admins
  - Full access to Admin operations

### 2. SuperAdmin
- **Role:** System-wide controller
- **Permissions:**
  - Full access to all system features and user accounts

### 3. Admin
- **Role:** Section manager
- **Permissions:**
  - Oversee StoreOwners and Customers
  - Manage assigned sections

### 4. StoreOwner
- **Role:** Store manager
- **Permissions:**
  - Manage inventory and related data
  - Create and publish articles

### 5. Customer
- **Role:** End user
- **Permissions:**
  - Browse and purchase products
  - Track order history

## Authentication & Login System
Provides a **secure login system** with role-based dashboards.

### Features:
- Username & Password Validation
- Multi-Factor Authentication (if enabled)
- Session & Token Management

### Role-Based Dashboards
Users are redirected to specific dashboards after authentication:
- **SuperAdmin Panel:** Manage system-wide settings, users, and reports
- **Admin Panel:** Oversee sections and monitor roles
- **StoreOwner Panel:** Manage inventory, track sales, publish articles
- **Customer Panel:** Explore products, make purchases, track orders

## API Endpoints

### 1. User Signup
- **Endpoint:** `/signup/` (POST)
- **Description:** Creates a new user (customer or store owner).
- **Request:**
  ```json
  {"username": "example", "password": "pass", "first_name": "John", "last_name": "Doe", "user_type": "customer"}
  ```
- **Response:**
  ```json
  {"success": "Customer created", "tokens": {"access": "<token>", "refresh": "<token>"}, "user": {"id": 1, "first_name": "John", "last_name": "Doe", "user_type": "customer"}}
  ```

### 2. User Login
- **Endpoint:** `/login_manual/` (POST)
- **Description:** Authenticates user with username and password.
- **Request:**
  ```json
  {"username": "example", "password": "pass"}
  ```
- **Response:**
  ```json
  {"success": "Login successful", "tokens": {"access": "<token>", "refresh": "<token>"}, "user": {"id": 1, "first_name": "John", "last_name": "Doe", "user_type": "customer"}}
  ```

### 3. JWT Token Validation
- **Endpoint:** `/login_JWT/` (POST)
- **Description:** Validates JWT token.
- **Request Header:**
  ```json
  {"Authorization": "Bearer <token>"}
  ```
- **Response:**
  ```json
  {"value": true}
  ```

### 4. Get User Information
- **Endpoint:** `/user_information/` (GET)
- **Description:** Retrieves authenticated user details.
- **Request Header:**
  ```json
  {"Authorization": "Bearer <token>"}
  ```
- **Response:**
  ```json
  {"user_data": {"id": 1, "first_name": "John", "last_name": "Doe", "user_type": "customer"}}
  ```

## Additional Information
- Uses **JWT Authentication**.
- Requires `Authorization` header for authenticated requests.
- Models include `CustomUser` and `CustomUserSerializer_Full`.
- Dependencies: Django REST Framework, Simple JWT.
- Future Development: Store listing API (`/stores_list/`).

