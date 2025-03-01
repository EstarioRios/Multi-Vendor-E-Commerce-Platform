# Authentication System Module

## Overview
The Authentication System module is a custom-built authentication solution for a multi-vendor platform. It is designed to handle user registration, login, and profile management using Django REST Framework and JWT (JSON Web Tokens). The system supports three types of users: Customers, Store Owners, and Admins.

---

## Key Features
1. **User Types**:
   - **Customers**: Regular users who can browse and purchase products.
   - **Store Owners**: Users who manage their own stores and products.
   - **Admins**: Superusers with administrative privileges.

2. **Authentication**:
   - Secure JWT-based authentication.
   - Access and refresh tokens for session management.
   - SMS-based verification for admin accounts.

3. **Validation**:
   - Phone number validation for Iranian numbers.
   - National code validation (10 digits).
   - File upload validation for store logos (max 2MB, JPG/PNG/JPEG formats).

4. **Custom User Model**:
   - Extends Django's `AbstractBaseUser` for flexibility.
   - Includes fields like `phone_number`, `national_code`, `store_logo`, and `industry`.

---

## How It Works
The Authentication System is built using Django and Django REST Framework. It uses a custom user model (`CustomUser`) to handle different user types and their specific requirements. The system provides endpoints for user registration, login, token validation, and profile management.

### Key Components
1. **CustomUser Model**:
   - Handles user data and roles.
   - Includes methods for creating customers, store owners, and admins.

2. **Authentication Flow**:
   - Users register via the `/signup/` endpoint.
   - Users log in using the `/login_manual` endpoint to receive JWT tokens.
   - Tokens are validated using the `/login_JWT` endpoint.
   - User information is retrieved using the `/user_information` endpoint.

3. **URL Configuration**:
   - All authentication-related URLs are defined in `AuthenticationSystem/urls.py`.
   - These URLs are included in the main project's `urls.py`.

---

## API Documentation

### 1. User Registration
- **Endpoint**: `POST /authentication/signup/`
- **Parameters**:
  - `user_type`: Type of user (customer/store_owner/admin).
  - `username`: Unique username.
  - `password`: User password.
  - `first_name`: User's first name.
  - `last_name`: User's last name.
  - `store_name`: Required for store owners.
  - `industry`: Required for store owners (ID of the industry).
- **Response**:
  - `tokens`: Access and refresh tokens.
  - `user`: Basic user information.

### 2. User Login
- **Endpoint**: `POST /authentication/login_manual`
- **Parameters**:
  - `username`: User's username.
  - `password`: User's password.
- **Response**:
  - `tokens`: Access and refresh tokens.
  - `user`: Basic user information.

### 3. Token Validation
- **Endpoint**: `POST /authentication/login_JWT`
- **Headers**:
  - `Authorization`: Bearer <access_token>
- **Response**:
  - Boolean value indicating token validity.

### 4. User Information
- **Endpoint**: `GET /authentication/user_information`
- **Headers**:
  - `Authorization`: Bearer <access_token>
- **Response**:
  - Detailed user information.

