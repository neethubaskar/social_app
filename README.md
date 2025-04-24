# 🧑‍🤝‍🧑 Social Backend API (Django)

This is a backend API for a social platform built using Django and Django REST Framework.  
It supports user registration (including Google OAuth), authentication with JWT, user profile management, friend suggestions, friend requests, and friend listings.

---

## 🚀 Features

- User Registration (Email & Google OAuth)
- JWT Authentication
- Profile View & Update
- Searchable Paginated User List
- Friend Suggestions (Mocked)
- Friend Requests (Send, Accept/Reject)
- List Accepted Friends

---

## 🔧 Tech Stack

- Python 3.10+
- Django 5.x
- Django REST Framework
- PostgreSQL or SQLite (default)
- djangorestframework-simplejwt (JWT Auth)
- python-decouple (for .env config)

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/neethubaskar/social_app.git
cd social_app
```
### Step 2: Create & Activate Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Requirements

```bash
pip install -r requirements.txt
```

### Step 4: Create .env File

```bash
DJANGO_SECRET_KEY=Your django secret key
DEBUG=False
DATABASES_NAME=Your database name
DATABASES_USER=Database user
DATABASES_PASSWORD=Database password
DATABASES_HOST=Database Host
DATABASES_PORT=Database Port
ALGORITHM=HS256
```

### Step 5: Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 6: Run Development Server

```bash
python manage.py runserver
```


## 🔐 Auth APIs

| Method | Endpoint                      | Description                              |
|--------|-------------------------------|------------------------------------------|
| POST   | `/users/api/v1/register/`     | Register with name, email, password      |
| POST   | `/users/api/v1/login/`        | Login and get JWT token                  |
| POST   | `/users/api/v1/google-login/` | Google OAuth2 login                      |
| GET    | `/users/api/v1/profile/`      | Get current user profile                 |
| PATCH  | `/users/api/v1/profile/`      | Update user profile                      |
| GET    |  `/users/api/v1/users/`       | List users with search option (?search=) |



