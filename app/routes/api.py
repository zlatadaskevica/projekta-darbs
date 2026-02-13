"""
API routes module
Defines API endpoints for fetching events and user data
Returns JSON responses
"""

from flask import Blueprint, jsonify, session, request
from app.models import Event, SavedEvent
from app.services.nasa import get_apod, get_neo_feed
from app.services.astronomy import get_moon_phase, calculate_visibility_for_latvia


# Create Blueprint for API routes
api_bp = Blueprint('api', __name__, url_prefix='/api')


def _get_event_id_from_request():
    """
    Reads event_id from JSON request body.
    Returns event_id or None.
    """

    data = request.get_json(silent=True) or {}

    return data.get('event_id')


@api_bp.route('/events', methods=['GET'])
def get_events():
    """
    API endpoint to get all events
    Returns JSON list of events
    """
    
    # Get all events from database
    events = Event.get_all()
    
    return jsonify({
        "success": True,
        "events": events
    })


@api_bp.route('/events/upcoming', methods=['GET'])
def get_upcoming_events():
    """
    API endpoint to get upcoming events
    Optional query parameter: limit (default: 10)
    """
    
    # Get limit from query parameters
    limit = request.args.get('limit', 10, type=int)
    
    # Get upcoming events
    events = Event.get_upcoming(limit=limit)
    
    return jsonify({
        "success": True,
        "count": len(events),
        "events": events
    })


@api_bp.route('/events/save', methods=['POST'])
def save_event():
    """
    API endpoint to save an event for user
    Requires authentication
    Request body: { "event_id": <id> }
    """
    
    # Check if user is logged in
    user_id = session.get('user_id')
    
    if not user_id:
        return jsonify({
            "success": False,
            "error": "Authentication required"
        }), 401
    
    # Get event ID from request
    event_id = _get_event_id_from_request()
    
    if not event_id:
        return jsonify({
            "success": False,
            "error": "Event ID is required"
        }), 400
    
    # Save event for user
    SavedEvent.save_event(user_id, event_id)
    
    return jsonify({
        "success": True,
        "message": "Event saved successfully"
    })


@api_bp.route('/events/unsave', methods=['POST'])
def unsave_event():
    """
    API endpoint to remove saved event
    Requires authentication
    Request body: { "event_id": <id> }
    """
    
    # Check if user is logged in
    user_id = session.get('user_id')
    
    if not user_id:
        return jsonify({
            "success": False,
            "error": "Authentication required"
        }), 401
    
    # Get event ID from request
    event_id = _get_event_id_from_request()
    
    if not event_id:
        return jsonify({
            "success": False,
            "error": "Event ID is required"
        }), 400
    
    # Remove saved event
    SavedEvent.remove_saved_event(user_id, event_id)
    
    return jsonify({
        "success": True,
        "message": "Event removed from saved"
    })


@api_bp.route('/nasa/apod', methods=['GET'])
def nasa_apod():
    """
    API endpoint to get NASA Astronomy Picture of the Day
    Optional query parameter: date (format: YYYY-MM-DD)
    """
    
    # Get date from query parameters
    date = request.args.get('date', None)
    
    # Get APOD data
    apod_data = get_apod(date=date)
    
    if apod_data:
        return jsonify({
            "success": True,
            "data": apod_data
        })
    else:
        return jsonify({
            "success": False,
            "error": "Failed to fetch APOD data"
        }), 500


@api_bp.route('/nasa/neo', methods=['GET'])
def nasa_neo():
    """
    API endpoint to get Near Earth Objects data
    Required query parameters: start_date, end_date (format: YYYY-MM-DD)
    """
    
    # Get date range from query parameters
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    if not start_date or not end_date:
        return jsonify({
            "success": False,
            "error": "start_date and end_date are required"
        }), 400
    
    # Get NEO data
    neo_data = get_neo_feed(start_date, end_date)
    
    return jsonify({
        "success": True,
        "count": len(neo_data),
        "data": neo_data
    })


@api_bp.route('/astronomy/moon-phase', methods=['GET'])
def moon_phase():
    """
    API endpoint to get current Moon phase
    Returns phase name, illumination, and angle
    """
    
    # Calculate Moon phase
    phase_data = get_moon_phase()
    
    return jsonify({
        "success": True,
        "data": phase_data
    })


@api_bp.route('/astronomy/visibility', methods=['GET'])
def moon_visibility():
    """
    API endpoint to get Moon visibility for Latvia
    Returns phase, rise/set times for Riga
    """
    
    # Calculate visibility for Latvia
    visibility_data = calculate_visibility_for_latvia()
    
    return jsonify({
        "success": True,
        "data": visibility_data
    })
