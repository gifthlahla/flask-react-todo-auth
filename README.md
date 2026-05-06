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

```
fastapi-react-todo-app/
├── backend/
│ ├── main.py                    # FastAPI app, endpoints, logging, CORS
│ ├── database.py                # SQLite connection and table creation
│ ├── models.py                  # Pydantic models for request/response
│ └── requirements.txt           # Python dependencies
├── frontend/
│ ├── src/
│ │ ├── components/
│ │ │ ├── Login.tsx
│ │ │ ├── Register.tsx
│ │ │ └── Protected.tsx
│ │ ├── services/
│ │ │ └── api.ts                 # API call helpers with token injection
│ │ ├── App.tsx                  # React Router routes
│ │ ├── main.tsx
│ │ └── index.css                # Tailwind CSS import
│ ├── package.json
│ ├── tailwind.config.js         # (if using Tailwind v3)
│ ├── vite.config.ts
│ └── ...
└── README.md
```

## Setup and Installation

### Prerequisites

- Python 3.8 or higher
- Node.js 18+ and npm
- Git

### Backend

1. **Navigate to the backend folder**
   ```bash
   cd backend
2. **Create and activate a virtual environment (recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt

4. **Run the server**
   ```bash
   uvicorn main:app --reload --port 8000

The API will be available at `http://localhost:8000`. The SQLite database (app.db) and app.log will be created automatically in the backend/ folder on first run.

### Frontend

1. **Navigate to the frontend folder**
   ```bash
   cd frontend

2. **Install npm packages**
   ```bash
   npm install

3. **Start the development server**
   ```bash
   npm run dev

The React app will open at `http://localhost:3000`.

## API Endpoints
| Method | Endpoint | Description	| Auth Required |
|----------|-------|----------------------------------|--------------|
| POST | /register | Create a new user account | No |
| POST | /login | Authenticate and receive a token | No |
| GET | /protected | Access protected content (dummy) | Bearer Token |
