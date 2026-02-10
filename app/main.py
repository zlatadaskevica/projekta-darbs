"""
Main application file
Entry point of the Flask web application
Initializes app, loads configuration, and registers routes
"""

from flask import Flask
from app.config import Config
from app.database import init_database
from app.routes.pages import pages_bp
from app.routes.api import api_bp


def create_app():
    """
    Application factory
    Creates and configures Flask application
    """
    
    # Create Flask app instance
    app = Flask(__name__, template_folder='templates', static_folder='../static')
    
    # Load configuration
    app.config.from_object(Config)
    
    # Validate configuration
    Config.validate()
    
    # Initialize database connection
    init_database()
    
    # Register blueprints (route modules)
    app.register_blueprint(pages_bp)
    app.register_blueprint(api_bp)
    
    return app


# Create application instance
app = create_app()


if __name__ == '__main__':
    """
    Run application in development mode
    """
    
    # Start Flask development server
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
