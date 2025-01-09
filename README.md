# Django Project

## Description

This project is a Django-based web application that provides a RESTful API using Django Rest Framework (DRF). It implements token-based authentication with `authtoken` and uses PostgreSQL as its database backend.

Thanks to this backend project, we can do these actions:

- Each team will be able to produce the parts they are responsible for.
- Teams will be able to view the parts they have produced.
- The Assembly team will be able to produce an aircraft:
  - First, create an aircraft.
  - Then, assemble the parts into the aircraft.
  - Finally, complete the aircraft production.
- The produced aircraft will be listable.

##### _Postman collection can be used by importing Aircraft Production.postman_collection file located in backend folder._

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
