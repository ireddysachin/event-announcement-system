

from flask import Flask, jsonify, render_template, request
from database import get_connection, initialize_database
import sqlite3


app = Flask(__name__)

initialize_database()



with get_connection() as connection:
    sample_events = [
        (
            "DevOps Workshop",
            "2026-11-15",
            "Bengaluru",
            "Learn the basics of CI/CD and automation.",
        ),
        (
            "Cloud Computing Meetup",
            "2026-11-20",
            "Online",
            "Explore cloud infrastructure and deployment.",
        ),
    ]

    for event in sample_events:
        connection.execute(
            """
            INSERT INTO events (title, date, location, description)
            SELECT ?, ?, ?, ?
            WHERE NOT EXISTS (
                SELECT 1 FROM events WHERE title = ?
            )
            """,
            (*event, event[0]),
        )



# Temporary sample event data for Day 2
events = [
    {
        "id": 1,
        "title": "DevOps Workshop",
        "date": "2026-11-15",
        "location": "Bengaluru",
        "description": "Learn the basics of CI/CD and automation."
    },
    {
        "id": 2,
        "title": "Cloud Computing Meetup",
        "date": "2026-11-20",
        "location": "Online",
        "description": "Explore cloud infrastructure and deployment."
    }
]

# Temporary in-memory subscriber list
subscribers = []


@app.route("/")
def home():
    with get_connection() as connection:
        rows = connection.execute(
            "SELECT id, title, date, location, description "
            "FROM events ORDER BY date, id"
        ).fetchall()

    events = [dict(row) for row in rows]

    return render_template("index.html", events=events)



@app.route("/api/events", methods=["GET"])
def get_events():
    with get_connection() as connection:
        rows = connection.execute(
            "SELECT id, title, date, location, description FROM events ORDER BY id"
        ).fetchall()

    return jsonify([dict(row) for row in rows])



@app.route("/api/events", methods=["POST"])
def create_event():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "success": False,
            "message": "Request body must be valid JSON."
        }), 400

    required_fields = ["title", "date", "location", "description"]

    for field in required_fields:
        if not isinstance(data.get(field), str) or not data[field].strip():
            return jsonify({
                "success": False,
                "message": f"{field} is required."
            }), 400


    new_event = {
        "title": data["title"].strip(),
        "date": data["date"].strip(),
        "location": data["location"].strip(),
        "description": data["description"].strip(),
    }

    
    with get_connection() as connection:
        existing_event = connection.execute(
            """
            SELECT id FROM events
            WHERE LOWER(title) = LOWER(?)
              AND date = ?
              AND LOWER(location) = LOWER(?)
            """,
            (
                new_event["title"],
                new_event["date"],
                new_event["location"],
            ),
        ).fetchone()

        if existing_event:
            return jsonify({
                "success": False,
                "message": "This event already exists for that date and location.",
            }), 409

        
        cursor = connection.execute(
            """
            INSERT INTO events (title, date, location, description)
            VALUES (?, ?, ?, ?)
            """,
            (
                new_event["title"],
                new_event["date"],
                new_event["location"],
                new_event["description"],
            ),
        )

        new_event["id"] = cursor.lastrowid

    return jsonify({
        "success": True,
        "message": "Event created successfully!",
        "event": new_event,
    }), 201








@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "application": "Event Announcement System"
    })



@app.route("/subscribe", methods=["POST"])
def subscribe():
    data = request.get_json(silent=True) or {}
    email = data.get("email", "")

    if not isinstance(email, str):
        email = ""

    email = email.strip().lower()

    # Validate the email address.
    if (
        not email
        or "@" not in email
        or "." not in email.split("@")[-1]
        or " " in email
    ):
        return jsonify({
            "success": False,
            "message": "Please enter a valid email address."
        }), 400

    # Save the subscriber permanently in SQLite.
    try:
        with get_connection() as connection:
            connection.execute(
                "INSERT INTO subscribers (email) VALUES (?)",
                (email,)
            )
            connection.commit()

    except sqlite3.IntegrityError:
        return jsonify({
            "success": False,
            "message": "This email is already subscribed."
        }), 409

    return jsonify({
        "success": True,
        "message": "Subscription successful!"
    }), 201




if __name__ == "__main__":
    app.run(debug=True, port=5000)
