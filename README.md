# Astronomy & Space Events Tracker

This project is a Python web application that tracks astronomy and space-related events
for users in Latvia, using public APIs and astronomical calculations.

The application includes:
- User authentication
- A database with multiple related tables
- Integration with external APIs (NASA API)
- Astronomical calculations (e.g. Moon phases)
- Clean, readable, and well-structured Python code

## Tech Stack
- Python
- Flask (backend)
- Supabase (PostgreSQL database)
- NASA Open API
- Skyfield (astronomical calculations)

---

## Project Structure and File Responsibilities

### app/main.py
Entry point of the application.
Initializes the web app, loads configuration, and registers routes.

### app/config.py
Loads environment variables and application configuration.
No hardcoded secrets.

### app/database.py
Handles database connection to Supabase.
Contains database client initialization.

### app/models.py
Defines data models and data access logic.
Represents tables: users, events, saved_events.

### app/auth.py
Handles user registration and login.
Includes password hashing and basic access protection.

### app/services/nasa.py
Responsible for communication with NASA API.
Fetches Astronomy Picture of the Day and other space data.

### app/services/astronomy.py
Contains astronomical calculations.
Used for Moon phases and visibility logic.

### app/routes/pages.py
Defines routes that render HTML pages for users.

### app/routes/api.py
Defines API endpoints for fetching events and user data.

### app/templates/
Contains HTML templates.
Only presentation logic, no business logic.

### static/
Contains static files such as CSS.

---

## Coding Style and Best Practices (IMPORTANT)

When generating code, ALWAYS follow these rules:

- Each statement must be written on a new line
- Separate logical code blocks (conditions, loops, lists) with an empty line
- Use indentation consistently to show structure
- Avoid long lines; split lines to improve readability
- Use meaningful variable and function names
  (e.g. `event_date` instead of `d`)
- Add comments explaining:
  - logical blocks
  - purpose of conditions and loops
  - role of the code section (e.g. data fetching, data output)

The code must be:
- readable
- beginner-friendly
- logically structured
- suitable for a school project
