# JewelaryManagement System

This is a Django backend project for managing jewelry business operations. It features a custom user model with Admin and Staff roles, registration and login APIs, JWT authentication, and role-based permissions.

## Features
- Custom user model: id, name, employee_id, date_of_joining, username, password, address, phone_number, role
- Registration and login APIs (using Django REST Framework APIView)
- JWT authentication (access and refresh tokens)
- Role-based permissions (isAdmin, isAuthenticated)
- Database migrations

## Setup Instructions
1. Install dependencies: Django, djangorestframework, djangorestframework-simplejwt
2. Run migrations
3. Start the development server

## Usage
- Register and login endpoints available via API
- JWT tokens returned on successful login
- Admin and Staff roles supported

---

Replace this README with more details as you build out the project.