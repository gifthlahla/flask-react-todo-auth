# Full-Stack To-Do Application (Auth + Protected Route)

A full-stack web application built as part of a Computer Science competency test. The backend (Python 3.8+, FastAPI) provides user registration, login with token‑based authentication, and a protected endpoint, all logged to `app.log`. The frontend (React 18 + TypeScript + Tailwind CSS) offers registration/login forms, stores the auth token, accesses a protected page, and handles logout.

## Features

- **User Registration** – Secure password storage (SHA-256 hashed) in SQLite.
- **Login** – Returns a random bearer token; stored client‑side.
- **Protected Route** – Verifies token; displays a welcome message.
- **Logging** – All requests and errors recorded in `backend/app.log`.
- **CORS** – Enabled for `http://localhost:3000`.
- **TypeScript Strict Typing** – No `any` types; `useState`, `useEffect`, loading and error states displayed.
- **Minimal, Responsive UI** – Styled with Tailwind CSS.

## Tech Stack

| Layer    | Technology                          |
|----------|-------------------------------------|
| Backend  | Python 3.8+, FastAPI, SQLite        |
| Frontend | React 18+, TypeScript, Vite, Tailwind CSS |
| Auth     | Random Bearer token (stored in DB)  |
| Logging  | Python’s built‑in `logging` module  |

## Project Structure

```text
fastapi-react-todo-app/
├── backend/
│   ├── app/                    # Backend modular python packages
│   │   ├── auth.py             # Auth helpers (hashing, tokens, verify)
│   │   ├── database.py         # DB connection & initialization
│   │   └── models.py           # Pydantic schemas
│   ├── main.py                 # FastAPI app configuration & route handlers
│   ├── requirements.txt        # Backend dependencies
│   └── app.db                  # SQLite database (created on startup)
└── frontend/
    ├── src/
    │   ├── components/         # React components (Login, Register, Protected)
    │   ├── services/           # API fetch services
    │   ├── App.tsx             # Route settings
    │   └── main.tsx            # Application entrypoint
    ├── tailwind.config.js      # Tailwind configuration
    └── package.json            # Node dependencies & run scripts
```

## Setup and Installation

### Prerequisites

- Python 3.8 or higher
- Node.js 18+ and npm
- Git

### Backend Setup

1. **Navigate to the backend folder**:
   ```bash
   cd backend
   ```

2. **Create and activate a virtual environment (recommended)**:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install the dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Start the FastAPI backend server**:
   ```bash
   uvicorn main:app --reload --port 8000
   ```
   The backend API documentation will be available at `http://127.0.0.1:8000/docs`.

### Frontend Setup

1. **Navigate to the frontend folder**:
   ```bash
   cd frontend
   ```

2. **Install the dependencies**:
   ```bash
   npm install
   ```

3. **Start the Vite development server**:
   ```bash
   npm run dev
   ```
   The application will be running at `http://localhost:3000`.

## API Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST   | `/register` | Create a new user account | No |
| POST   | `/login` | Authenticate and receive a token | No |
| GET    | `/protected` | Access protected content | Yes (Bearer Token) |
