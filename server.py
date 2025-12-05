# ==========================================================
# Babylon Reservation Backend
# Clean, stable, and production-ready
# ==========================================================

import os
import re
import uuid
import sqlite3
import datetime
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
from flask import Flask, request, jsonify

import requests  # for SendGrid API

# ----------------------------------------------------------
# Load environment
# ----------------------------------------------------------
load_dotenv()

DB_FILE = os.getenv("DB_FILE", "reservations.db")

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY", "").strip()
EMAIL_FROM = os.getenv("EMAIL_FROM", "").strip()

SMTP_HOST = os.getenv("SMTP_HOST", "").strip()
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "").strip()
SMTP_PASS = os.getenv("SMTP_PASS", "").strip()

# Fallback: if EMAIL_FROM is empty, use SMTP_USER
if not EMAIL_FROM and SMTP_USER:
    EMAIL_FROM = SMTP_USER

# ----------------------------------------------------------
# Flask setup
# ----------------------------------------------------------
app = Flask(__name__, static_folder=".", static_url_path="")

# ----------------------------------------------------------
# Database init
# ----------------------------------------------------------
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS reservations (
            id TEXT PRIMARY KEY,
            created_at TEXT,
            name TEXT,
            phone TEXT,
            email TEXT,
            guests INTEGER,
            date TEXT,
            time TEXT,
            status TEXT,
            email_status TEXT
        );
    """)
    conn.commit()
    conn.close()

# ----------------------------------------------------------
# Validation
# ----------------------------------------------------------
def valid_phone(p):
    return bool(re.match(r'^\+?\d{7,15}$', p))

def valid_email(e):
    return bool(re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", e))

# ----------------------------------------------------------
# Time window validation (11:30 AM – 11:00 PM)
# ----------------------------------------------------------
def convert_to_24h(t):
    return datetime.datetime.strptime(t, "%I:%M %p").time()

OPEN_TIME = convert_to_24h("11:30 AM")
CLOSE_TIME = convert_to_24h("11:00 PM")

def is_allowed_time(t):
    try:
        tt = convert_to_24h(t)
        return OPEN_TIME <= tt <= CLOSE_TIME
    except:
        return False

# ----------------------------------------------------------
# Premium HTML email template
# ----------------------------------------------------------
def build_email_html(name, date, time, guests):
    return f"""
    <div style="font-family:Arial, sans-serif;padding:20px;background:#fff7fb;">
      <div style="max-width:540px;margin:auto;background:white;padding:20px;border-radius:12px;
                  border:1px solid #f3dae6;box-shadow:0 6px 24px rgba(0,0,0,0.07);">
        <h2 style="color:#ff5f95;margin:0 0 6px 0;font-size:24px;font-weight:700;">Babylon Reservation</h2>
        <p style="color:#4b3c40;font-size:15px;margin-top:14px;">
          Hi <b>{name}</b>,<br><br>
          Your reservation request has been received. Our team will confirm shortly.
        </p>

        <div style="margin-top:16px;padding:14px;background:#fff0f7;border-radius:10px;border:1px solid #f7d3e4;">
          <p style="margin:0;font-size:14px;color:#333;">
            <b>Date:</b> {date}<br>
            <b>Time:</b> {time}<br>
            <b>Guests:</b> {guests}
          </p>
        </div>

        <p style="color:#6d5a5f;font-size:14px;margin-top:18px;">
          Thank you for choosing Babylon.<br>
          <b>We look forward to hosting you.</b>
        </p>
      </div>
    </div>
    """

# ----------------------------------------------------------
# Send email (SendGrid first, SMTP fallback)
# ----------------------------------------------------------
def send_email(to_email, subject, html_content):
    # Try SendGrid
    if SENDGRID_API_KEY:
        resp = requests.post(
            "https://api.sendgrid.com/v3/mail/send",
            headers={"Authorization": f"Bearer {SENDGRID_API_KEY}",
                     "Content-Type": "application/json"},
            json={
                "personalizations": [{
                    "to": [{"email": to_email}],
                    "subject": subject
                }],
                "from": {"email": EMAIL_FROM},
                "content": [
                    {"type": "text/html", "value": html_content}
                ]
            },
            timeout=10
        )

        if resp.status_code in [200, 202]:
            return True, "sent (SendGrid)"
        else:
            print("SendGrid Error:", resp.text)

    # If no SendGrid or failed → try SMTP
    if SMTP_USER and SMTP_PASS:
        try:
            msg = MIMEText(html_content, "html")
            msg["Subject"] = subject
            msg["From"] = EMAIL_FROM
            msg["To"] = to_email

            s = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
            s.starttls()
            s.login(SMTP_USER, SMTP_PASS)
            s.sendmail(EMAIL_FROM, [to_email], msg.as_string())
            s.quit()
            return True, "sent (SMTP)"
        except Exception as e:
            print("SMTP ERROR:", e)
            return False, f"error: {e}"

    return False, "no email service configured"

# ----------------------------------------------------------
# ROUTES
# ----------------------------------------------------------

@app.route("/")
def home():
    return app.send_static_file("index.html")

@app.route("/reserve", methods=["POST"])
def reserve():
    # AJAX detection
    is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest"

    name = request.form.get("name", "").strip()
    phone = request.form.get("phone", "").strip()
    email = request.form.get("email", "").strip()
    guests = request.form.get("guests", "").strip()
    date = request.form.get("date", "").strip()
    time = request.form.get("time", "").strip()
    confirm18 = request.form.get("confirm")

    # Validation
    if not name or not phone or not email or not guests or not date or not time:
        return jsonify({"success": False, "message": "Missing fields"}), 400

    if not valid_phone(phone):
        return jsonify({"success": False, "message": "Invalid phone number"}), 400

    if not valid_email(email):
        return jsonify({"success": False, "message": "Invalid email"}), 400

    if confirm18 is None:
        return jsonify({"success": False, "message": "18+ confirmation required"}), 400

    if not is_allowed_time(time):
        return jsonify({"success": False, "message": "Reservations allowed only between 11:30 AM and 11:00 PM"}), 400

    # Insert into DB
    rid = str(uuid.uuid4())
    created = datetime.datetime.now().isoformat()

    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO reservations (id, created_at, name, phone, email, guests, date, time, status, email_status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (rid, created, name, phone, email, guests, date, time, "pending", "not sent"))
    conn.commit()
    conn.close()

    # Send email
    html_message = build_email_html(name, date, time, guests)
    ok, status = send_email(email, "Your Babylon Reservation Request", html_message)

    # Update DB with email status
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("UPDATE reservations SET email_status=? WHERE id=?", (status, rid))
    conn.commit()
    conn.close()

    # JSON response for modal
    return jsonify({
        "success": True,
        "name": name,
        "date": date,
        "time": time,
        "email_status": status
    })

# ----------------------------------------------------------
# Static file helper (CSS, JS, images)
# ----------------------------------------------------------
@app.route("/<path:path>")
def static_proxy(path):
    return app.send_static_file(path)

# ----------------------------------------------------------
# Run
# ----------------------------------------------------------
if __name__ == "__main__":
    init_db()
    print("Babylon server running on http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000, debug=True)
