# Astronomy & Space Events Tracker

A Flask web app where users can:

- register and log in
- view astronomy/space events
- save events to a personal list (`saved_events`)
- see NASA APOD and astronomy calculations

## Stack

- Python + Flask
- Supabase (tables: `users`, `events`, `saved_events`)
- NASA Open API
- Skyfield

## Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Create `.env` from template:

```bash
cp .env.example .env
```

3. Fill in values in `.env`:

- `SUPABASE_URL`
- `SUPABASE_KEY`
- `NASA_API_KEY`
- `SECRET_KEY`

4. In Supabase SQL editor, run:

- `supabase_schema.sql`

5. Start app:

```bash
python -m app.main
```

Open: `http://localhost:5000`

## Notes

- If `events` table is empty, the app auto-loads initial events from NASA NEO feed.
- Users can save/unsave events from `/events`.
