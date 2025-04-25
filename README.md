https://roadmap.sh/projects/expense-tracker-api

# 💸 Expense Tracker API

A simple RESTful API built with Flask to manage user authentication and personal expense tracking. This project includes JWT-based authentication, user registration/login, and CRUD operations for managing expenses.

## 🚀 Features

- User registration and login
- JWT-based authentication and token validation
- Middleware to protect private routes
- Expense creation, retrieval, and listing per user
- SQLite database integration via SQLAlchemy
- Flask Blueprints for modular route management

## 🏗️ Project Structure

```
expense-tracker-api/
│
├── app.py                       # Main application entry point
├── config.py                   # App configuration (e.g., secret keys, DB URI)
├── data.db                     # SQLite database (generated on first run)
│
├── controllers/                # Route controllers
│   ├── auth_controller.py      # Handles login and registration
│   └── expense_controller.py   # Handles expense-related routes
│
├── middleware/                 
│   └── auth_middleware.py      # Token validation middleware
│
├── models.py                   # SQLAlchemy models (User, Expense)
├── requirements.txt            # Project dependencies
└── .env                        # Environment variables (e.g., secret keys)
```

## 📦 Requirements

- Python 3.8+
- Flask
- Flask-CORS
- PyJWT
- SQLAlchemy
- python-dotenv


## 🚀 Running the Application

### 🔧 Prerequisites

Install dependencies:

```bash
pip install -r requirements.txt
```

---

### 🖥️ 1. Run the Flask Backend

Start your Flask API server:

```bash
python app.py
```

The backend will start running at:

```
http://localhost:5555
```

---

### 💻 2. Run the Streamlit Frontend

In a **new terminal**, launch the Streamlit UI:

```bash
streamlit run app_frontend.py
```

This will open the app in your browser at:

```
http://localhost:8501
```

If it doesn't open automatically, you can manually navigate to that URL.


The server will start at `http://127.0.0.1:5555`.

## 🔐 Authentication

All protected routes require a **JWT token** passed in the `Authorization` header:

```
Authorization: Bearer <your_token>
```

## 📫 API Endpoints

### Auth Routes

| Method | Endpoint        | Description           |
|--------|------------------|-----------------------|
| POST   | `/auth/register` | Register a new user   |
| POST   | `/auth/login`    | Login and get a token |

### Expense Routes (JWT Protected)

| Method | Endpoint     | Description                   |
|--------|---------------|-------------------------------|
| POST   | `/expense/`   | Add a new expense             |
| GET    | `/expense/`   | Get all expenses for the user |

## 🔒 Middleware

JWT validation is handled by the `@token_required` decorator in `auth_middleware.py`, ensuring protected routes can only be accessed by authenticated users.

## 🛠️ To Do

- Update/Delete expense endpoints   
- Pagination for large expense lists  
- Token refresh system

## 📄 License

MIT License

---

Built with ❤️ using Flask.
