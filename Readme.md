# Setting Up PostgreSQL for Django

## Prerequisites

- **Python 3.10+**
- **Django 4.2+**
- **PostgreSQL 14+**
- **psycopg2** (PostgreSQL adapter for Python)

---

## 1. Install PostgreSQL

- **macOS (using Homebrew)**:
    ```bash
    brew install postgresql
    brew services start postgresql
    ```

- **Ubuntu**:
    ```bash
    sudo apt update
    sudo apt install postgresql postgresql-contrib
    sudo systemctl start postgresql
    ```

---

## 2. Create Database and User

1. **Access PostgreSQL shell**:
    ```bash
    psql postgres
    ```

2. **Create a new database and user**:
    ```sql
    CREATE DATABASE api_db;
    CREATE USER django_users WITH PASSWORD 'your_password';
    ALTER ROLE django_users SET client_encoding TO 'utf8';
    ALTER ROLE django_users SET default_transaction_isolation TO 'read committed';
    ALTER ROLE django_users SET timezone TO 'UTC';
    GRANT ALL PRIVILEGES ON DATABASE api_db TO django_users;
    ```

3. **Exit PostgreSQL shell**:
    ```sql
    \q
    ```

---

## 3. Configure Django to Use PostgreSQL

Update the `DATABASES` setting in your Django `settings.py` file:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'api_db',
        'USER': 'django_users',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

# Setting Up PostgreSQL for Django

## Prerequisites

- **Python 3.10+**
- **Django 4.2+**
- **PostgreSQL 14+**
- **psycopg2** (PostgreSQL adapter for Python)

---

## 4. Install PostgreSQL Driver (psycopg2)

Install `psycopg2` to enable Django to connect to PostgreSQL:

```bash
pip install psycopg2
```
## 5. Run Migrations
After configuring the database, run migrations to set up the database schema:

```bash
python manage.py makemigrations
python manage.py migrate

```

# API Transactions Service

API Transactions Service is a Django-based REST API designed for user authentication, balance management (top-up, payments, and transfers), and viewing transaction history.

## Features

- **User Registration and Login** with phone number and PIN.
- **JWT Authentication** for secure API access.
- **Balance Management**: Top-up, payments, and transfers between users.
- **Transaction Reporting**: View all user transactions.
- **User Profile Management**: Update profile information.

## Requirements

- Python 3.10 or higher
- Django 4.2 or higher
- Django REST Framework
- djangorestframework-simplejwt

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/username/api_transactions.git
    cd api_transactions
    ```

2. Create a virtual environment:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows use .venv\Scripts\activate
    ```

3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Apply the database migrations:
    ```bash
    python manage.py migrate
    ```

5. Run the development server:
    ```bash
    python manage.py runserver
    ```

## API Endpoints

### User Registration

- **URL**: `/register/`
- **Method**: `POST`
- **Request**:
    ```json
    {
        "phone_number": "08123456789",
        "first_name": "John",
        "last_name": "Doe",
        "address": "Jl. Sudirman No. 1",
        "pin": "1234"
    }
    ```
- **Response**:
    ```json
    {
        "status": "SUCCESS",
        "result": {
            "user_id": "123e4567-e89b-12d3-a456-426614174000",
            "first_name": "John",
            "last_name": "Doe",
            "phone_number": "08123456789",
            "address": "Jl. Sudirman No. 1"
        }
    }
    ```

### User Login

- **URL**: `/login/`
- **Method**: `POST`
- **Request**:
    ```json
    {
        "phone_number": "08123456789",
        "pin": "1234"
    }
    ```
- **Response**:
    ```json
    {
        "status": "SUCCESS",
        "result": {
            "access_token": "{jwt_token}",
            "refresh_token": "{refresh_token}"
        }
    }
    ```

### Top-Up Balance

- **URL**: `/topup/`
- **Method**: `POST`
- **Headers**: `Authorization: Bearer {JWT_Token}`
- **Request**:
    ```json
    {
        "amount": 100000
    }
    ```
- **Response**:
    ```json
    {
        "status": "SUCCESS",
        "result": {
            "top_up_id": "201ddde1-f797-484b-b1a0-07d1190e790a",
            "amount": 100000,
            "balance_before": 0,
            "balance_after": 100000,
            "created_date": "2024-09-28 12:01:21"
        }
    }
    ```

### Make Payment

- **URL**: `/pay/`
- **Method**: `POST`
- **Headers**: `Authorization: Bearer {JWT_Token}`
- **Request**:
    ```json
    {
        "amount": 100000,
        "remarks": "Payment for service"
    }
    ```
- **Response**:
    ```json
    {
        "status": "SUCCESS",
        "result": {
            "payment_id": "13bcb11c-111e-4a65-9afd-90a86a01cd21",
            "amount": 100000,
            "remarks": "Payment for service",
            "balance_before": 500000,
            "balance_after": 400000,
            "created_date": "2024-09-28 12:05:00"
        }
    }
    ```

### Transfer Balance

- **URL**: `/transfer/`
- **Method**: `POST`
- **Headers**: `Authorization: Bearer {JWT_Token}`
- **Request**:
    ```json
    {
        "target_user": "b7342e8e-e8e7-4a5d-873e-b1b1bfcdeddb",
        "amount": 30000,
        "remarks": "Gift"
    }
    ```
- **Response**:
    ```json
    {
        "status": "SUCCESS",
        "result": {
            "transfer_id": "a7d39cf6-44b6-41fc-b3e9-7b16df5321c5",
            "amount": 30000,
            "remarks": "Gift",
            "balance_before": 400000,
            "balance_after": 370000,
            "created_date": "2024-09-28 12:06:20"
        }
    }
    ```

### Transaction Report

- **URL**: `/transactions/`
- **Method**: `GET`
- **Headers**: `Authorization: Bearer {JWT_Token}`
- **Response**:
    ```json
    {
        "status": "SUCCESS",
        "result": [
            {
                "transfer_id": "a7d39cf6-44b6-41fc-b3e9-7b16df5321c5",
                "transaction_type": "DEBIT",
                "amount": 30000,
                "remarks": "Gift",
                "balance_before": 400000,
                "balance_after": 370000,
                "created_date": "2024-09-28 12:06:20"
            },
            {
                "payment_id": "13bcb11c-111e-4a65-9afd-90a86a01cd21",
                "transaction_type": "DEBIT",
                "amount": 100000,
                "remarks": "Payment for service",
                "balance_before": 500000,
                "balance_after": 400000,
                "created_date": "2024-09-28 12:05:00"
            }
        ]
    }
    ```

### Profile Update

- **URL**: `/profile/`
- **Method**: `PUT`
- **Headers**: `Authorization: Bearer {JWT_Token}`
- **Request**:
    ```json
    {
        "first_name": "Tom",
        "last_name": "Araya",
        "address": "Jl. Diponegoro No. 215"
    }
    ```
- **Response**:
    ```json
    {
        "status": "SUCCESS",
        "result": {
            "user_id": "bc1c823e-b0fb-4b20-88c0-dff25e283252",
            "first_name": "Tom",
            "last_name": "Araya",
            "address": "Jl. Diponegoro No. 215",
            "updated_date": "2024-09-28 12:08:00"
        }
    }
    ```

## Authentication

JWT (JSON Web Token) authentication is used throughout the API for secure access. Upon a successful login, you will receive an access token and a refresh token. The access token is used to authenticate subsequent API requests.

### Using the Access Token

Use the `access_token` in the `Authorization` header for any authenticated request:


### Example: Using the Access Token in cURL
bash
Copy code
curl --location --request GET 'http://127.0.0.1:8000/transactions/' \
--header 'Authorization: Bearer {jwt_token}'