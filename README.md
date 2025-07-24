python -m app.main

## 🧪 Example API Usage

### Filter users by company and city
...

### Filter users by hosted and attended count with pagination and sorting

curl -X GET "http://127.0.0.1:8000/api/v1/users/filter?attended_min=2" -H "accept: application/json"

curl -X GET "http://127.0.0.1:8000/api/v1/users/filter?hosted_min=1&hosted_max=5&attended_min=0&attended_max=3&sort_by=created_at&sort_dir=desc&skip=0&limit=10" -H "accept: application/json"


for sending email
curl -X POST "http://127.0.0.1:8000/api/v1/users/send-email-smtp" \
-H "Content-Type: application/json" \
-d '{
  "subject": "SMTP Email Test",
  "content": "This is a test sent via Gmail SMTP.",
  "filters": {
    "company": "Grab",
    "city": "Singapore",
    "hosted_min": 1,
    "hosted_max": 5
  }
}'

# 🧩 Event CRM – FastAPI Backend

A scalable CRM backend using **FastAPI** and **SQLAlchemy** to manage user data, event participation, and targeted email campaigns.

---

## ✅ Features

- 🧑‍💼 **User & Event Management**
- 🧾 Filter users by:
  - Company, Job title, City, State
  - #Events Hosted / Attended (with range)
- 📬 Send email to filtered users (SMTP supported)
- 📈 Track email status via `EmailLog` table
- ⚡ Efficient queries with joins, subqueries, pagination
- 🧩 Clean architecture: routers, services, models, utils

---

## 🏗️ System Architecture

app/
├── api/v1/routes/         # FastAPI routers
│   └── users_route.py     # User-related endpoints
├── core/
│   └── log_config.py      # JSON logging config
├── db/
│   ├── base.py            # SQLAlchemy base
│   └── session.py         # DB session manager
├── models/
│   ├── user_model.py      # User & EmailLog SQLAlchemy models
│   └── event_model.py     # Event & event-user relationships
├── schemas/
│   └── user_schema.py     # Pydantic schemas for API I/O
├── services/
│   └── user_service.py    # Business logic (filter, analytics)
├── utils/
│   └── email_util.py      # SMTP email sender
└── main.py                # FastAPI app entry
github/workflow
├── ci.yml/# Config it run on github action

---

## 🧪 API Endpoints

| Method | Endpoint                      | Description                           |
|--------|-------------------------------|---------------------------------------|
| GET    | `/api/v1/users/filter`        | Filter users by query, pagination, sorting|
| POST   | `/api/v1/users/send-email-smtp` | Send email via SMTP (e.g. Gmail)    |
| GET    | `/`                           | Health check root 
---

## 📊 Efficient Querying

- Counts hosted/attended events using **subqueries + joins**
- Filters include **range queries** (`hosted_min`, `attended_max`, etc.)
- Uses `offset`, `limit`, `order_by` for **pagination/sorting**

---

## 📬 Email Tracking

- Logs each sent email in `EmailLog` table
- Tracks:
  - `user_id`, `subject`, `content`, `status`, `created_at`
- Example log record:

```json
{
  "user_id": "123",
  "subject": "Welcome",
  "status": "sent",
  "created_at": "2025-07-24T12:34:56"
}

⚙️ Config & Setup
## Run it on local
    1. 📦 Set up dependencies
        ~ python3.13 -m venv venv
        ~ source venb/bin/activate (Mac/Linux) - venv\Scripts\activate (Windows)
        ~ pip install -r requirements.txt
    2. 🔑 Environment Variables (.env)
        EMAIL_SENDER=your_email@gmail.com
        EMAIL_PASSWORD=your_gmail_app_password
    3. 🚀 Run the App
        ~ uvicorn app.main:app --reload
## Run it as docker
    1. Build the image
    ~ docker build -t event-crm-app .

    2. Run the container
    docker run -p 8000:8000 event-crm-app

🧠 Decisions & Assumptions
	•	EmailLog is used for basic analytics; extendable to track bounces or open rate.
	•	No external mail services (SendGrid, etc.) used to keep it simple.
	•	App is built without Alembic; DB is managed manually or by raw SQL setup.
	•	Uses SQLite for local dev. Easily swappable for PostgreSQL.

👨‍💻 Author
	•	Brian Huynh – Event ERM assignment -FastAPI Developer, 2025