"""
Authentication module
Handles user registration and login
Includes password hashing and verification
"""

import bcrypt
from app.models import User


def hash_password(password):
    """
    Hashes a password using bcrypt
    Returns hashed password as string
    """
    
    # Generate salt and hash password
    salt = bcrypt.gensalt()
    password_bytes = password.encode('utf-8')
    hashed = bcrypt.hashpw(password_bytes, salt)
    
    # Return as string for database storage
    return hashed.decode('utf-8')


def verify_password(password, password_hash):
    """
    Verifies if password matches the hash
    Returns True if password is correct, False otherwise
    """
    
    # Convert to bytes for comparison
    password_bytes = password.encode('utf-8')
    hash_bytes = password_hash.encode('utf-8')
    
    # Check password against hash
    return bcrypt.checkpw(password_bytes, hash_bytes)


def register_user(email, username, password):
    """
    Registers a new user
    Returns user data if successful, None if user already exists
    """
    
    # Check if user with this email already exists
    existing_user = User.find_by_email(email)
    
    if existing_user:
        return None
    
    # Hash the password
    password_hash = hash_password(password)
    
    # Create new user in database
    user_data = User.create(email, username, password_hash)
    
    return user_data


def login_user(email, password):
    """
    Authenticates a user
    Returns user data if credentials are correct, None otherwise
    """
    
    # Find user by email
    user = User.find_by_email(email)
    
    if not user:
        return None
    
    # Verify password
    if not verify_password(password, user['password_hash']):
        return None
    
    # Return user data without password hash
    user_data = {
        'id': user['id'],
        'email': user['email'],
        'username': user['username']
    }
    
    return user_data
