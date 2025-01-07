# Django Project

## Description

This project is a Django-based web application that provides a RESTful API using Django Rest Framework (DRF). It implements token-based authentication with `authtoken` and uses PostgreSQL as its database backend.

---

## Features

- **RESTful API**: Built with Django Rest Framework (DRF) to enable easy communication between the frontend and backend.
- **Token-based Authentication**: Secures API endpoints using Django's `authtoken`.
- **PostgreSQL Database**: Uses `psycopg2-binary` to interact with a PostgreSQL database.

---

## Prerequisites

Ensure you have the following installed on your system:

- Python 3.8+
- PostgreSQL
- pip (Python package manager)

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/alikilicw/aircraft-production-backend
cd aircraft-production-backend
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure PostgreSQL

1. Create a PostgreSQL database.
2. Update the `DATABASES` section in `settings.py` with your database credentials:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': '<database-name>',
           'USER': '<database-user>',
           'PASSWORD': '<database-password>',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

### 5. Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create a Superuser

```bash
python manage.py createsuperuser
```

### 7. Run the Server

```bash
python manage.py runserver
```

---
