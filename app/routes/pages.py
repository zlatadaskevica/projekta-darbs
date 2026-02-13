"""
Page routes module
Defines routes that render HTML pages for users
"""

from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from app.auth import register_user, login_user
from app.models import Event, SavedEvent
from app.services.nasa import get_apod
from app.services.astronomy import get_moon_phase, calculate_visibility_for_latvia
from app.services.event_loader import ensure_events_available


# Create Blueprint for page routes
pages_bp = Blueprint('pages', __name__)


def _get_saved_event_ids_for_user(user_id):
    """
    Returns a list of event IDs saved by the user.
    """

    saved_events = SavedEvent.get_user_saved_events(user_id)

    return [saved_event['event_id'] for saved_event in saved_events]


@pages_bp.route('/')
def index():
    """
    Home page
    Shows astronomy information and upcoming events
    """
    
    # Ensure that events are available for users
    ensure_events_available()

    # Get NASA Astronomy Picture of the Day
    apod_data = get_apod()
    
    # Get current Moon phase
    moon_phase = get_moon_phase()
    
    # Get Moon visibility for Latvia
    visibility_info = calculate_visibility_for_latvia()
    
    # Get upcoming events
    upcoming_events = Event.get_upcoming(limit=5)
    
    # Check if user is logged in
    user_id = session.get('user_id')
    
    return render_template(
        'index.html',
        apod=apod_data,
        moon_phase=moon_phase,
        visibility=visibility_info,
        events=upcoming_events,
        user_id=user_id
    )


@pages_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    Registration page
    Handles user registration
    """
    
    if request.method == 'POST':
        # Get form data
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Validate input
        if not email or not username or not password:
            flash('All fields are required', 'error')
            return render_template('register.html')
        
        # Register user
        user_data = register_user(email, username, password)
        
        if user_data:
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('pages.login'))
        else:
            flash('User with this email already exists', 'error')
            return render_template('register.html')
    
    return render_template('register.html')


@pages_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Login page
    Handles user authentication
    """
    
    if request.method == 'POST':
        # Get form data
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Validate input
        if not email or not password:
            flash('Email and password are required', 'error')
            return render_template('login.html')
        
        # Authenticate user
        user_data = login_user(email, password)
        
        if user_data:
            # Store user ID in session
            session['user_id'] = user_data['id']
            session['username'] = user_data['username']
            
            flash(f'Welcome, {user_data["username"]}!', 'success')
            return redirect(url_for('pages.index'))
        else:
            flash('Invalid email or password', 'error')
            return render_template('login.html')
    
    return render_template('login.html')


@pages_bp.route('/logout')
def logout():
    """
    Logout
    Clears user session
    """
    
    # Clear session
    session.clear()
    
    flash('You have been logged out', 'info')
    return redirect(url_for('pages.index'))


@pages_bp.route('/events')
def events():
    """
    Events page
    Shows all astronomy events
    """
    
    # Ensure that events are available for users
    ensure_events_available()

    # Get all events
    all_events = Event.get_all()
    
    # Check if user is logged in
    user_id = session.get('user_id')
    
    # Get user's saved events if logged in
    saved_event_ids = []

    if user_id:
        saved_event_ids = _get_saved_event_ids_for_user(user_id)
    
    return render_template(
        'events.html',
        events=all_events,
        saved_event_ids=saved_event_ids,
        user_id=user_id
    )


@pages_bp.route('/my-events')
def my_events():
    """
    User's saved events page
    Shows events saved by current user
    """
    
    # Check if user is logged in
    user_id = session.get('user_id')
    
    if not user_id:
        flash('Please log in to view your saved events', 'error')
        return redirect(url_for('pages.login'))
    
    # Get user's saved events
    saved_events = SavedEvent.get_user_saved_events(user_id)
    
    return render_template(
        'my_events.html',
        saved_events=saved_events
    )
