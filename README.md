# 📚 Library Service API

A scalable RESTful API for modern library management, built with **Django** and **Django REST Framework**.

Supports:
- User registration & JWT authentication
- Book inventory management (full CRUD)
- Borrowing and returning flow
- Stripe-based payment integration
- Telegram notifications for user/library events
- Asynchronous tasks & reminders (Celery + Celery Beat)
- Convenient task monitoring via Flower
- Out-of-the-box setup with Docker (PostgreSQL by default, SQLite for development possible)

---

## 🧪 Technology Stack

- Python 3.10+
- Django & Django REST Framework
- PostgreSQL (or SQLite for local development)
- Celery & Redis
- Docker (with Compose)
- Flower (optional dashboard)
- Telegram integration via pyTelegramBotAPI

---

## 🚀 Features

- JWT-based authentication (registration & login)
- Full CRUD for books, inventory tracking
- Borrowing/return operations, tied to user
- Payment workflow using Stripe
- Telegram bot integration (user-specific link)
- Asynchronous notifications via Celery
- Daily overdue reminders with Celery Beat
- Flower dashboard for Celery task monitoring
- Fully dockerized for easy setup and deployment

---

## 🧱 Models Overview

| Model       | Description                                          |
|-------------|------------------------------------------------------|
| `User`      | Custom user (email auth, Telegram fields)            |
| `Book`      | Title, author, cover, inventory count, daily fee     |
| `Borrowing` | Tracks who borrowed which book and when              |
| `Payment`   | Linked to borrowing, handles payment states          |

---

## ⚙️ Business Logic

- **Permissions:** Users can only view/update their own borrowings/data
- **Notifications:** Asynchronous notifications with Celery + Telegram
- **Scheduling:** Daily reminders on overdue borrowings
- **Signals:** Django signals trigger notifications on borrow/create/payment events
- **Validation:** Borrowing only possible if Telegram username is set in profile

---

## 🐳 Docker (recommended)

```bash
git clone https://github.com/TrMaksym/Library-Service.git

cd social-media-api
cp .env.sample .env
docker-compose up --build
```
git clone https://github.com/TrMaksym/Library-Service.git

## Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate   # On Windows use: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.sample .env
# Edit `.env` and fill in your secrets

# Apply migrations
python manage.py migrate

# Run development server
python manage.py runserver
```
