from fastapi import FastAPI, HTTPException, Request, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import logging
import sys
import hashlib
import secrets
import sqlite3
import os
from datetime import datetime
from contextlib import contextmanager
from typing import Optional, Dict

# ============== CONFIGURATION ==============
DATABASE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app.db")

# ============== LOGGING ==============
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# ============== DATABASE ==============
def get_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

@contextmanager
def get_db():
    conn = get_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def init_db():
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tokens (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                token TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
            )
        """)
        conn.commit()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise
    finally:
        conn.close()

# ============== AUTH HELPERS ==============
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def generate_token() -> str:
    return secrets.token_hex(32)

def create_user(username: str, password: str) -> bool:
    password_hash = hash_password(password)
    with get_db() as db:
        try:
            db.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username, password_hash)
            )
            logger.info(f"User created: {username}")
            return True
        except sqlite3.IntegrityError:
            logger.warning(f"Username already exists: {username}")
            return False

def authenticate_user(username: str, password: str) -> Optional[str]:
    password_hash = hash_password(password)
    with get_db() as db:
        user = db.execute(
            "SELECT id, username FROM users WHERE username = ? AND password_hash = ?",
            (username, password_hash)
        ).fetchone()
        
        if not user:
            logger.warning(f"Failed login attempt for: {username}")
            return None
        
        token = generate_token()
        db.execute(
            "INSERT INTO tokens (user_id, token) VALUES (?, ?)",
            (user["id"], token)
        )
        logger.info(f"User logged in: {username}")
        return token

def verify_token(token: str) -> Optional[Dict]:
    with get_db() as db:
        user_data = db.execute("""
            SELECT users.id, users.username
            FROM tokens
            JOIN users ON tokens.user_id = users.id
            WHERE tokens.token = ?
        """, (token,)).fetchone()
        
        if not user_data:
            logger.warning(f"Invalid token used: {token[:10]}...")
            return None
        
        logger.info(f"Token verified for user: {user_data['username']}")
        return {"id": user_data["id"], "username": user_data["username"]}

# ============== MODELS ==============
class UserRegister(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6, max_length=128)

class UserLogin(BaseModel):
    username: str
    password: str

# ============== FASTAPI APP ==============
app = FastAPI(title="To-Do App API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = datetime.now()
    logger.info(f"{request.method} {request.url.path}")
    response = await call_next(request)
    duration = (datetime.now() - start_time).total_seconds()
    logger.info(f"{response.status_code} ({duration:.3f}s)")
    return response

# Startup event
@app.on_event("startup")
async def startup():
    init_db()
    logger.info("Application started successfully")

# Routes
@app.get("/")
async def root():
    return {"status": "online", "message": "API is running"}

@app.post("/register", status_code=201)
async def register(user: UserRegister):
    logger.info(f"Registration attempt: {user.username}")
    if not create_user(user.username, user.password):
        raise HTTPException(status_code=400, detail="Username already exists")
    return {"message": "User created successfully"}

@app.post("/login")
async def login(user: UserLogin):
    logger.info(f"Login attempt: {user.username}")
    token = authenticate_user(user.username, user.password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"access_token": token, "token_type": "bearer"}

@app.get("/protected")
async def protected_route(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    token = authorization.split(" ")[1]
    user_data = verify_token(token)
    if not user_data:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    return {
        "message": f"Welcome {user_data['username']}! This is a protected page.",
        "username": user_data['username']
    }