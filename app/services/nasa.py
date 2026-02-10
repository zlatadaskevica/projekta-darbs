"""
NASA API service
Handles communication with NASA Open APIs
"""

import requests
from app.config import Config


def get_apod(date=None):
    """
    Gets Astronomy Picture of the Day from NASA
    
    Parameters:
    date - optional date in format YYYY-MM-DD
    
    Returns dictionary with:
    - title: image title
    - explanation: description
    - url: image URL
    - date: image date
    """
    
    # NASA APOD API endpoint
    api_url = "https://api.nasa.gov/planetary/apod"
    
    # Prepare request parameters
    params = {
        "api_key": Config.NASA_API_KEY
    }
    
    # Add date parameter if provided
    if date:
        params["date"] = date
    
    try:
        # Make request to NASA API
        response = requests.get(api_url, params=params, timeout=10)
        
        # Check if request was successful
        response.raise_for_status()
        
        # Parse JSON response
        data = response.json()
        
        return {
            "title": data.get("title"),
            "explanation": data.get("explanation"),
            "url": data.get("url"),
            "date": data.get("date"),
            "media_type": data.get("media_type", "image")
        }
    
    except requests.exceptions.RequestException as e:
        # Handle request errors
        print(f"Error fetching NASA APOD: {e}")
        return None


def get_neo_feed(start_date, end_date):
    """
    Gets Near Earth Objects data from NASA
    
    Parameters:
    start_date - start date in format YYYY-MM-DD
    end_date - end date in format YYYY-MM-DD
    
    Returns list of near Earth objects
    """
    
    # NASA NEO Feed API endpoint
    api_url = "https://api.nasa.gov/neo/rest/v1/feed"
    
    # Prepare request parameters
    params = {
        "api_key": Config.NASA_API_KEY,
        "start_date": start_date,
        "end_date": end_date
    }
    
    try:
        # Make request to NASA API
        response = requests.get(api_url, params=params, timeout=10)
        
        # Check if request was successful
        response.raise_for_status()
        
        # Parse JSON response
        data = response.json()
        
        # Extract NEO data
        neo_list = []
        near_earth_objects = data.get("near_earth_objects", {})
        
        # Process each date
        for date_key in near_earth_objects:
            objects_on_date = near_earth_objects[date_key]
            
            # Add each object to list
            for obj in objects_on_date:
                neo_list.append({
                    "name": obj.get("name"),
                    "date": date_key,
                    "diameter_km": obj.get("estimated_diameter", {}).get("kilometers", {}).get("estimated_diameter_max"),
                    "is_hazardous": obj.get("is_potentially_hazardous_asteroid", False),
                    "velocity_kph": obj.get("close_approach_data", [{}])[0].get("relative_velocity", {}).get("kilometers_per_hour")
                })
        
        return neo_list
    
    except requests.exceptions.RequestException as e:
        # Handle request errors
        print(f"Error fetching NASA NEO data: {e}")
        return []


def get_mars_weather():
    """
    Gets Mars weather data from NASA InSight mission
    Returns latest Mars weather information
    """
    
    # NASA InSight API endpoint
    api_url = "https://api.nasa.gov/insight_weather/"
    
    # Prepare request parameters
    params = {
        "api_key": Config.NASA_API_KEY,
        "feedtype": "json",
        "ver": "1.0"
    }
    
    try:
        # Make request to NASA API
        response = requests.get(api_url, params=params, timeout=10)
        
        # Check if request was successful
        response.raise_for_status()
        
        # Parse JSON response
        data = response.json()
        
        return data
    
    except requests.exceptions.RequestException as e:
        # Handle request errors
        print(f"Error fetching Mars weather: {e}")
        return None
