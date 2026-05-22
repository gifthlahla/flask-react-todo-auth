import hashlib
import secrets
import logging
from typing import Optional, Dict
from .database import get_db

logger = logging.getLogger(__name__)

def hash_password(password: str) -> str:
    """
    Hash a password using SHA-256.
    For production, use bcrypt or argon2 instead.
    """
    # Using SHA-256 with a salt would be better for production
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def generate_token() -> str:
    """Generate a cryptographically secure random token."""
    return secrets.token_hex(32)

def create_user(username: str, password: str) -> bool:
    """
    Create a new user in the database.
    Returns True if successful, False if username already exists.
    """
    password_hash = hash_password(password)
    
    with get_db() as db:
        try:
            db.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username, password_hash)
            )
            logger.info(f"User created: {username}")
            return True
        except Exception as e:
            if "UNIQUE constraint failed" in str(e):
                logger.warning(f"Username already exists: {username}")
                return False
            logger.error(f"Error creating user {username}: {e}")
            raise e

def authenticate_user(username: str, password: str) -> Optional[str]:
    """
    Authenticate a user and return a token if successful.
    Returns the token string, or None if authentication fails.
    """
    password_hash = hash_password(password)
    
    with get_db() as db:
        # Check if user exists with matching credentials
        user = db.execute(
            "SELECT id, username FROM users WHERE username = ? AND password_hash = ?",
            (username, password_hash)
        ).fetchone()
        
        if not user:
            logger.warning(f"Failed login attempt for: {username}")
            return None
        
        # Generate and store token
        token = generate_token()
        db.execute(
            "INSERT INTO tokens (user_id, token) VALUES (?, ?)",
            (user["id"], token)
        )
        
        logger.info(f"User logged in: {username}")
        return token

def verify_token(token: str) -> Optional[Dict]:
    """
    Verify a token and return user info if valid.
    Returns a dict with user id and username, or None if invalid.
    """
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
        return {
            "id": user_data["id"],
            "username": user_data["username"]
        }

def delete_token(token: str) -> None:
    """Delete a token (for logout)."""
    with get_db() as db:
        db.execute("DELETE FROM tokens WHERE token = ?", (token,))
        logger.info(f"Token deleted: {token[:10]}...")