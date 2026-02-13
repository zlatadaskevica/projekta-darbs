"""
Astronomy calculations service
Handles astronomical calculations using Skyfield library
Calculates Moon phases, visibility, and other astronomical events
"""

from datetime import datetime, timedelta
import math

from skyfield.api import load, wgs84


# Global cache for astronomy objects.
# They are loaded lazily so the app can still run if remote files are blocked.
ts = None
earth = None
moon = None
sun = None


def _initialize_skyfield():
    """
    Loads Skyfield resources only when needed.
    Returns True when loading succeeds, False otherwise.
    """

    global ts
    global earth
    global moon
    global sun

    if ts is not None and earth is not None and moon is not None and sun is not None:
        return True

    try:
        ephemeris = load('de421.bsp')

        earth = ephemeris['earth']
        moon = ephemeris['moon']
        sun = ephemeris['sun']
        ts = load.timescale()

        return True

    except OSError:
        return False


def _fallback_moon_phase(date):
    """
    Basic moon phase fallback.
    Uses a simple synodic cycle approximation.
    """

    cycle_days = 29.53058867
    known_new_moon = datetime(2000, 1, 6, 18, 14)

    elapsed_days = (date - known_new_moon).total_seconds() / 86400
    phase_position = (elapsed_days % cycle_days) / cycle_days

    elongation = phase_position * 360
    illumination = (1 - math.cos(math.radians(elongation))) / 2 * 100

    if elongation < 22.5 or elongation >= 337.5:
        phase_name = "New Moon"
    elif elongation < 67.5:
        phase_name = "Waxing Crescent"
    elif elongation < 112.5:
        phase_name = "First Quarter"
    elif elongation < 157.5:
        phase_name = "Waxing Gibbous"
    elif elongation < 202.5:
        phase_name = "Full Moon"
    elif elongation < 247.5:
        phase_name = "Waning Gibbous"
    elif elongation < 292.5:
        phase_name = "Last Quarter"
    else:
        phase_name = "Waning Crescent"

    return {
        "phase_name": phase_name,
        "illumination": round(illumination, 1),
        "phase_angle": round(elongation, 1)
    }


def get_moon_phase(date=None):
    """
    Calculates current Moon phase
    """

    if date is None:
        date = datetime.now()

    if not _initialize_skyfield():
        return _fallback_moon_phase(date)

    t = ts.utc(date.year, date.month, date.day, date.hour, date.minute)

    e = earth.at(t)
    s = e.observe(sun).apparent()
    m = e.observe(moon).apparent()

    elongation = s.separation_from(m).degrees
    illumination = (1 + math.cos(math.radians(elongation))) / 2 * 100

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

    current_date = datetime.now()

    for day_offset in range(30):
        check_date = current_date + timedelta(days=day_offset)
        phase_info = get_moon_phase(check_date)

        if phase_info["illumination"] > 99 and phase_info["phase_name"] == "Full Moon":
            return check_date

    return None


def get_moon_rise_set(latitude, longitude, date=None):
    """
    Calculates moonrise and moonset times for specific location
    """

    if date is None:
        date = datetime.now()

    if not _initialize_skyfield():
        return {
            "moonrise": None,
            "moonset": None
        }

    location = wgs84.latlon(latitude, longitude)

    times = []

    for hour in range(24):
        t = ts.utc(date.year, date.month, date.day, hour, 0)

        observer = earth + location
        moon_position = observer.at(t).observe(moon).apparent()
        altitude = moon_position.altaz()[0].degrees

        times.append((t, altitude))

    moonrise = None
    moonset = None

    for i in range(len(times) - 1):
        alt1 = times[i][1]
        alt2 = times[i + 1][1]

        if alt1 < 0 and alt2 >= 0:
            moonrise = times[i + 1][0].utc_datetime()

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

    latitude = 56.9496
    longitude = 24.1052

    moon_phase = get_moon_phase()
    rise_set = get_moon_rise_set(latitude, longitude)

    return {
        "location": "Riga, Latvia",
        "phase": moon_phase,
        "rise_set": rise_set
    }
