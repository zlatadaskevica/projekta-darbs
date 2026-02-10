"""
Database module
Handles connection to Supabase database
"""

from supabase import create_client, Client
from app.config import Config


# Global database client instance
supabase_client: Client = None


def init_database():
    """
    Initializes connection to Supabase database
    Creates and returns database client
    """
    
    global supabase_client
    
    # Create Supabase client with URL and API key
    supabase_client = create_client(
        Config.SUPABASE_URL,
        Config.SUPABASE_KEY
    )
    
    return supabase_client


def get_database():
    """
    Returns the database client instance
    Initializes if not already initialized
    """
    
    global supabase_client
    
    if supabase_client is None:
        init_database()
    
    return supabase_client
