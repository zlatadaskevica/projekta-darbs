"""
Astronomy calculations service
Handles astronomical calculations using Skyfield library
Calculates Moon phases, visibility, and other astronomical events
"""

from datetime import datetime, timedelta
from skyfield.api import load, wgs84
import math


# Load ephemeris data for calculations
ephemeris = load('de421.bsp')
earth = ephemeris['earth']
moon = ephemeris['moon']
sun = ephemeris['sun']

# Create timescale for date calculations
ts = load.timescale()


def get_moon_phase(date=None):
    """
    Calculates current Moon phase
    
    Parameters:
    date - optional date to calculate phase for (default: today)
    
    Returns:
    - phase_name: name of Moon phase
    - illumination: percentage of Moon illumination (0-100)
    - phase_angle: angle in degrees (0-360)
    """
    
    # Use provided date or current date
    if date is None:
        date = datetime.now()
    
    # Convert to Skyfield time
    t = ts.utc(date.year, date.month, date.day, date.hour, date.minute)
    
    # Calculate phase angle
    e = earth.at(t)
    s = e.observe(sun).apparent()
    m = e.observe(moon).apparent()
    
    # Calculate elongation (angle between Sun and Moon)
    elongation = s.separation_from(m).degrees
    
    # Calculate illumination percentage
    illumination = (1 + math.cos(math.radians(elongation))) / 2 * 100
    
    # Determine phase name based on angle
    if elongation < 45:
        phase_name = "New Moon"
    elif elongation < 90:
        phase_name = "Waxing Crescent"
    elif elongation < 135:
        phase_name = "First Quarter"
    elif elongation < 180:
        phase_name = "Waxing Gibbous"
    elif elongation < 225:
        phase_name = "Full Moon"
    elif elongation < 270:
        phase_name = "Waning Gibbous"
    elif elongation < 315:
        phase_name = "Last Quarter"
    else:
        phase_name = "Waning Crescent"
    
    return {
        "phase_name": phase_name,
        "illumination": round(illumination, 1),
        "phase_angle": round(elongation, 1)
    }


def get_next_full_moon():
    """
    Calculates date and time of next Full Moon
    Returns datetime object
    """
    
    # Start from current date
    current_date = datetime.now()
    
    # Check next 30 days
    for day_offset in range(30):
        check_date = current_date + timedelta(days=day_offset)
        
        # Get Moon phase for this date
        phase_info = get_moon_phase(check_date)
        
        # Check if it's full moon (illumination > 99%)
        if phase_info["illumination"] > 99 and phase_info["phase_name"] == "Full Moon":
            return check_date
    
    return None


def get_moon_rise_set(latitude, longitude, date=None):
    """
    Calculates moonrise and moonset times for specific location
    
    Parameters:
    latitude - observer's latitude in degrees
    longitude - observer's longitude in degrees
    date - date to calculate for (default: today)
    
    Returns:
    - moonrise: moonrise time
    - moonset: moonset time
    """
    
    # Use provided date or current date
    if date is None:
        date = datetime.now()
    
    # Create observer location
    location = wgs84.latlon(latitude, longitude)
    
    # Define time range for the day
    t0 = ts.utc(date.year, date.month, date.day, 0, 0)
    t1 = ts.utc(date.year, date.month, date.day, 23, 59)
    
    # Find moonrise and moonset times
    times = []
    
    # Sample every hour to find rise/set events
    for hour in range(24):
        t = ts.utc(date.year, date.month, date.day, hour, 0)
        
        # Calculate Moon altitude
        observer = earth + location
        moon_position = observer.at(t).observe(moon).apparent()
        altitude = moon_position.altaz()[0].degrees
        
        times.append((t, altitude))
    
    # Find rise and set times
    moonrise = None
    moonset = None
    
    for i in range(len(times) - 1):
        alt1 = times[i][1]
        alt2 = times[i + 1][1]
        
        # Check for rise (crosses horizon from below)
        if alt1 < 0 and alt2 >= 0:
            moonrise = times[i + 1][0].utc_datetime()
        
        # Check for set (crosses horizon from above)
        if alt1 >= 0 and alt2 < 0:
            moonset = times[i + 1][0].utc_datetime()
    
    return {
        "moonrise": moonrise,
        "moonset": moonset
    }


def calculate_visibility_for_latvia():
    """
    Calculates Moon visibility specifically for Latvia
    Uses Riga coordinates as reference point
    """
    
    # Riga, Latvia coordinates
    latitude = 56.9496
    longitude = 24.1052
    
    # Get current Moon phase
    moon_phase = get_moon_phase()
    
    # Get Moon rise and set times
    rise_set = get_moon_rise_set(latitude, longitude)
    
    return {
        "location": "Riga, Latvia",
        "phase": moon_phase,
        "rise_set": rise_set
    }
