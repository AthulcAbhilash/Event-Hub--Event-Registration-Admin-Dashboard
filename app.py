from flask import Flask, render_template, request, redirect, session, url_for, send_file
import json
import os
from datetime import datetime
from functools import wraps
from io import BytesIO
from openpyxl import Workbook
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "event_project_secret_key_2026"

DATA_FILE = "data.json"
EVENT_FILE = "events.json"
UPLOAD_FOLDER = os.path.join("static", "images")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin@123"


def ensure_files():
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump([], file, indent=4)

    if not os.path.exists(EVENT_FILE):
        default_events = [
            {
                "id": "evt1",
                "name": "Tech Fest",
                "description": "Explore cutting-edge innovations and discover the future of technology.",
                "image": "event1.jpg",
                "date": "2026-05-10"
            },
            {
                "id": "evt2",
                "name": "Workshop",
                "description": "Build practical real-world skills through guided hands-on sessions.",
                "image": "event2.jpg",
                "date": "2026-05-15"
            },
            {
                "id": "evt3",
                "name": "Seminar",
                "description": "Learn from experts, industry speakers, and inspiring sessions.",
                "image": "event3.jpg",
                "date": "2026-05-20"
            },
            {
                "id": "evt4",
                "name": "Hackathon",
                "description": "Compete, collaborate, and innovate under pressure with your team.",
                "image": "event4.jpg",
                "date": "2026-05-25"
            }
        ]
        save_events(default_events)


def load_json_file(filename, default_value):
    if not os.path.exists(filename):
        return default_value

    with open(filename, "r", encoding="utf-8") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return default_value


def save_json_file(filename, data):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def load_data():
    return load_json_file(DATA_FILE, [])


def save_data(data):
    save_json_file(DATA_FILE, data)


def load_events():
    events = load_json_file(EVENT_FILE, [])
    for event in events:
        event["display_date"] = format_event_date(event.get("date", ""))
    return events


def save_events(events):
    save_json_file(EVENT_FILE, events)


def format_event_date(date_str):
    if not date_str:
        return "Date not set"
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").strftime("%d %b %Y")
    except ValueError:
        return date_str


def admin_login_required(route_function):
    @wraps(route_function)
    def wrapper(*args, **kwargs):
        if not session.get("admin_logged_in"):
            return redirect(url_for("admin_login"))
        return route_function(*args, **kwargs)
    return wrapper


def get_event_counts(registrations):
    event_counts = {}
    for item in registrations:
        event_name = item.get("event", "Unknown")
        event_counts[event_name] = event_counts.get(event_name, 0) + 1
    return event_counts


def allowed_image(filename):
    allowed_extensions = {"png", "jpg", "jpeg", "webp", "gif"}
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extensions


ensure_files()


@app.route("/")
def index():
    events = load_events()
    return render_template("index.html", events=events)


@app.route("/register", methods=["POST"])
def register():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    phone = request.form.get("phone", "").strip()
    event = request.form.get("event", "").strip()

    if not name or not email or not phone or not event:
        return redirect(url_for("index"))

    registrations = load_data()
    registrations.append({
        "id": datetime.now().strftime("%Y%m%d%H%M%S%f"),
        "name": name,
        "email": email,
        "phone": phone,
        "event": event,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
    })
    save_data(registrations)

    return redirect(url_for("index"))


@app.route("/admin-login", methods=["GET", "POST"])
def admin_login():
    error_message = ""

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["admin_logged_in"] = True
            session["admin_username"] = username
            return redirect(url_for("admin_dashboard"))

        error_message = "Invalid username or password."

    return render_template("admin_login.html", error_message=error_message)


@app.route("/logout")
@admin_login_required
def logout():
    session.clear()
    return redirect(url_for("admin_login"))


@app.route("/admin")
@admin_login_required
def admin_dashboard():
    registrations = load_data()
    events = load_events()
    event_counts = get_event_counts(registrations)

    return render_template(
        "view.html",
        data=registrations,
        total_registrations=len(registrations),
        event_counts=event_counts,
        events=events,
        admin_username=session.get("admin_username", "Admin")
    )


@app.route("/add-event", methods=["POST"])
@admin_login_required
def add_event():
    name = request.form.get("name", "").strip()
    description = request.form.get("description", "").strip()
    date = request.form.get("date", "").strip()
    image_file = request.files.get("image")

    if not name or not description or not date or not image_file or image_file.filename == "":
        return redirect(url_for("admin_dashboard"))

    if not allowed_image(image_file.filename):
        return redirect(url_for("admin_dashboard"))

    filename = f"{datetime.now().strftime('%Y%m%d%H%M%S%f')}_{secure_filename(image_file.filename)}"
    image_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    image_file.save(image_path)

    events = load_events()
    events.append({
        "id": datetime.now().strftime("evt%Y%m%d%H%M%S%f"),
        "name": name,
        "description": description,
        "image": filename,
        "date": date
    })
    save_events(events)

    return redirect(url_for("admin_dashboard"))


@app.route("/edit-event/<event_id>", methods=["POST"])
@admin_login_required
def edit_event(event_id):
    events = load_events()

    name = request.form.get("name", "").strip()
    description = request.form.get("description", "").strip()
    date = request.form.get("date", "").strip()
    image_file = request.files.get("image")

    for event in events:
        if event.get("id") == event_id:
            event["name"] = name
            event["description"] = description
            event["date"] = date

            if image_file and image_file.filename != "" and allowed_image(image_file.filename):
                filename = f"{datetime.now().strftime('%Y%m%d%H%M%S%f')}_{secure_filename(image_file.filename)}"
                image_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                image_file.save(image_path)
                event["image"] = filename

            event.pop("display_date", None)
            break

    for event in events:
        event.pop("display_date", None)

    save_events(events)
    return redirect(url_for("admin_dashboard"))


@app.route("/delete-event/<event_id>")
@admin_login_required
def delete_event(event_id):
    events = load_events()
    updated_events = []

    for event in events:
        if event.get("id") != event_id:
            event.pop("display_date", None)
            updated_events.append(event)

    save_events(updated_events)
    return redirect(url_for("admin_dashboard"))


@app.route("/delete/<entry_id>")
@admin_login_required
def delete_registration(entry_id):
    registrations = load_data()
    updated_registrations = [item for item in registrations if item.get("id") != entry_id]
    save_data(updated_registrations)
    return redirect(url_for("admin_dashboard"))


@app.route("/export-excel")
@admin_login_required
def export_excel():
    registrations = load_data()

    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Registrations"

    headers = ["ID", "Name", "Email", "Phone", "Event", "Date"]
    sheet.append(headers)

    for item in registrations:
        sheet.append([
            item.get("id", ""),
            item.get("name", ""),
            item.get("email", ""),
            item.get("phone", ""),
            item.get("event", ""),
            item.get("date", "")
        ])

    excel_file = BytesIO()
    workbook.save(excel_file)
    excel_file.seek(0)

    filename = f"event_registrations_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"

    return send_file(
        excel_file,
        as_attachment=True,
        download_name=filename,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


if __name__ == "__main__":
    app.run(debug=True)
