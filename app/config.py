"""
Configuration module
Loads environment variables and application settings
"""

import os
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()


class Config:
    """
    Application configuration class
    Stores all configuration parameters
    """
    
    # Supabase database configuration
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    
    # NASA API configuration
    NASA_API_KEY = os.getenv("NASA_API_KEY")
    
    # Flask secret key for sessions
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    
    @staticmethod
    def validate():
        """
        Validates that all required configuration parameters are set
        """
        
        if not Config.SUPABASE_URL:
            raise ValueError("SUPABASE_URL is not set in environment variables")
        
        if not Config.SUPABASE_KEY:
            raise ValueError("SUPABASE_KEY is not set in environment variables")
        
        if not Config.NASA_API_KEY:
            raise ValueError("NASA_API_KEY is not set in environment variables")
