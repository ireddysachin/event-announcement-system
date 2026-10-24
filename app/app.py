

from flask import Flask, jsonify, render_template, request
from database import get_connection, initialize_database
import sqlite3
from s3_storage import upload_banner, get_banner
from sns_notifications import publish_event_notification


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
            "SELECT id, title, date, location, description, banner_uri "
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
    data = request.get_json(silent=True) or {}
    banner_uri = data.get("banner_uri", "").strip()

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
        "banner_uri": data.get("banner_uri", "").strip(),
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
            INSERT INTO events (title, date, location, description, banner_uri)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                new_event["title"],
                new_event["date"],
                new_event["location"],
                new_event["description"],
                new_event["banner_uri"],
            ),
        )

        
        new_event["id"] = cursor.lastrowid

    try:
        message = (
            f"New Event: {new_event['title']}\n"
            f"Date: {new_event['date']}\n"
            f"Location: {new_event['location']}\n"
            f"Description: {new_event['description']}"
        )

        publish_event_notification(
            subject=f"New Event: {new_event['title']}",
            message=message,
        )
    except Exception:
        app.logger.exception(
            "Event was saved, but SNS notification failed"
        )

    


    return jsonify({
        "success": True,
        "message": "Event created successfully!",
        "event": new_event,
    }), 201


@app.route("/api/banners", methods=["POST"])
def upload_event_banner():
    if "banner" not in request.files:
        return jsonify({
            "success": False,
            "message": "Please select a banner image."
        }), 400

    banner = request.files["banner"]

    if not banner.filename:
        return jsonify({
            "success": False,
            "message": "Please select a banner image."
        }), 400

    allowed_types = {"image/jpeg", "image/png", "image/webp"}

    if banner.mimetype not in allowed_types:
        return jsonify({
            "success": False,
            "message": "Only JPEG, PNG, and WebP images are allowed."
        }), 400

    banner.seek(0, 2)
    file_size = banner.tell()
    banner.seek(0)

    if file_size > 5 * 1024 * 1024:
        return jsonify({
            "success": False,
            "message": "Banner image must be 5 MB or smaller."
        }), 400

    import uuid
    from werkzeug.utils import secure_filename

    extension = secure_filename(banner.filename).rsplit(".", 1)

    if len(extension) != 2:
        return jsonify({
            "success": False,
            "message": "Invalid image filename."
        }), 400

    object_key = f"event-banners/{uuid.uuid4().hex}.{extension[1].lower()}"

    try:
        object_uri = upload_banner(
            banner,
            object_key,
            banner.mimetype
        )
    except Exception:
        app.logger.exception("Banner upload failed")
        return jsonify({
            "success": False,
            "message": "Unable to upload banner. Please try again."
        }), 502

    return jsonify({
        "success": True,
        "message": "Banner uploaded successfully!",
        "object_uri": object_uri
    }), 201



@app.route("/banners/<path:filename>")
def serve_banner(filename):
    from flask import Response

    try:
        image_data, content_type = get_banner(filename)
        return Response(
            image_data,
            mimetype=content_type,
            headers={"Cache-Control": "no-cache"},
        )
    except Exception:
        app.logger.exception("Failed to retrieve banner from S3")
        return "Banner image not found", 404




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
