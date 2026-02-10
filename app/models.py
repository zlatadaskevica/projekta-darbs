"""
Data models module
Represents database tables and data access logic
Tables: users, events, saved_events
"""

from app.database import get_database


class User:
    """
    User model
    Represents users table in database
    """
    
    @staticmethod
    def create(email, username, password_hash):
        """
        Creates a new user in database
        Returns created user data
        """
        
        db = get_database()
        
        # Insert new user into users table
        response = db.table("users").insert({
            "email": email,
            "username": username,
            "password_hash": password_hash
        }).execute()
        
        return response.data
    
    @staticmethod
    def find_by_email(email):
        """
        Finds user by email address
        Returns user data or None if not found
        """
        
        db = get_database()
        
        # Query users table for matching email
        response = db.table("users").select("*").eq("email", email).execute()
        
        if response.data and len(response.data) > 0:
            return response.data[0]
        
        return None
    
    @staticmethod
    def find_by_id(user_id):
        """
        Finds user by ID
        Returns user data or None if not found
        """
        
        db = get_database()
        
        # Query users table for matching ID
        response = db.table("users").select("*").eq("id", user_id).execute()
        
        if response.data and len(response.data) > 0:
            return response.data[0]
        
        return None


class Event:
    """
    Event model
    Represents astronomy and space events table
    """
    
    @staticmethod
    def get_all():
        """
        Gets all events from database
        Returns list of events
        """
        
        db = get_database()
        
        # Select all events ordered by date
        response = db.table("events").select("*").order("event_date").execute()
        
        return response.data
    
    @staticmethod
    def get_upcoming(limit=10):
        """
        Gets upcoming events
        Returns limited number of future events
        """
        
        db = get_database()
        
        # Select upcoming events, ordered by date, limited
        response = db.table("events").select("*").order("event_date").limit(limit).execute()
        
        return response.data
    
    @staticmethod
    def create(title, description, event_date, event_type):
        """
        Creates a new event in database
        Returns created event data
        """
        
        db = get_database()
        
        # Insert new event into events table
        response = db.table("events").insert({
            "title": title,
            "description": description,
            "event_date": event_date,
            "event_type": event_type
        }).execute()
        
        return response.data


class SavedEvent:
    """
    Saved event model
    Represents user's saved events (many-to-many relationship)
    """
    
    @staticmethod
    def save_event(user_id, event_id):
        """
        Saves an event for a specific user
        Creates relationship between user and event
        """
        
        db = get_database()
        
        # Insert into saved_events table
        response = db.table("saved_events").insert({
            "user_id": user_id,
            "event_id": event_id
        }).execute()
        
        return response.data
    
    @staticmethod
    def get_user_saved_events(user_id):
        """
        Gets all events saved by a specific user
        Returns list of saved events
        """
        
        db = get_database()
        
        # Query saved_events and join with events table
        response = db.table("saved_events").select("*, events(*)").eq("user_id", user_id).execute()
        
        return response.data
    
    @staticmethod
    def remove_saved_event(user_id, event_id):
        """
        Removes a saved event for a user
        Deletes the relationship
        """
        
        db = get_database()
        
        # Delete from saved_events table
        response = db.table("saved_events").delete().eq("user_id", user_id).eq("event_id", event_id).execute()
        
        return response.data
