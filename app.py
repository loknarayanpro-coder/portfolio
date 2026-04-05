from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import json
from datetime import datetime
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

app = Flask(__name__)
CORS(app)

# ─── Config ───────────────────────────────────────────────────────────────────
# Set these as environment variables on your hosting platform
EMAIL_USER     = os.environ.get("EMAIL_USER", "")        # your gmail
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD", "")    # app password
EMAIL_TO       = os.environ.get("EMAIL_TO", "loknarayanpro@gmail.com")

SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "")

if SUPABASE_URL and SUPABASE_KEY:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
else:
    supabase = None

MESSAGES_FILE = "messages.json"

# ─── Helpers ──────────────────────────────────────────────────────────────────
def load_messages():
    if supabase:
        try:
            response = supabase.table("messages").select("*").execute()
            return response.data
        except Exception as e:
            print(f"Supabase error: {e}")
            return []
    else:
        if os.path.exists(MESSAGES_FILE):
            with open(MESSAGES_FILE, "r") as f:
                return json.load(f)
        return []

def save_message(data):
    if supabase:
        try:
            supabase.table("messages").insert({
                "name": data.get("name"),
                "email": data.get("email"),
                "subject": data.get("subject", "No Subject"),
                "service": data.get("service", ""),
                "message": data.get("message")
            }).execute()
        except Exception as e:
            print(f"Supabase insert error: {e}")
    else:
        messages = load_messages()
        messages.append({
            "id": len(messages) + 1,
            "name": data.get("name"),
            "email": data.get("email"),
            "subject": data.get("subject", "No Subject"),
            "service": data.get("service", ""),
            "message": data.get("message"),
            "timestamp": datetime.now().isoformat()
        })
        with open(MESSAGES_FILE, "w") as f:
            json.dump(messages, f, indent=2)

def send_email(data):
    if not EMAIL_USER or not EMAIL_PASSWORD:
        return False
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"[Portfolio] {data.get('subject', 'New Message')} — from {data.get('name')}"
        msg["From"]    = EMAIL_USER
        msg["To"]      = EMAIL_TO
        html = f"""
        <div style="font-family:sans-serif;max-width:600px;margin:0 auto;background:#0f0f0f;color:#f0ede8;padding:32px;border-radius:8px;">
          <h2 style="color:#c8f53f;margin-bottom:24px;">New Portfolio Message</h2>
          <table style="width:100%;border-collapse:collapse;">
            <tr><td style="padding:10px 0;color:#5a5a5a;width:100px;">Name</td><td style="padding:10px 0;">{data.get('name')}</td></tr>
            <tr><td style="padding:10px 0;color:#5a5a5a;">Email</td><td style="padding:10px 0;">{data.get('email')}</td></tr>
            <tr><td style="padding:10px 0;color:#5a5a5a;">Service</td><td style="padding:10px 0;">{data.get('service','—')}</td></tr>
            <tr><td style="padding:10px 0;color:#5a5a5a;vertical-align:top;">Message</td><td style="padding:10px 0;">{data.get('message')}</td></tr>
          </table>
          <p style="color:#5a5a5a;font-size:12px;margin-top:24px;">{datetime.now().strftime('%d %b %Y, %I:%M %p')}</p>
        </div>
        """
        msg.attach(MIMEText(html, "html"))
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_USER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_USER, EMAIL_TO, msg.as_string())
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False

# ─── Routes ───────────────────────────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/contact", methods=["POST"])
def contact():
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "error": "No data"}), 400

    required = ["name", "email", "message"]
    for field in required:
        if not data.get(field, "").strip():
            return jsonify({"success": False, "error": f"{field} is required"}), 400

    save_message(data)
    email_sent = send_email(data)

    return jsonify({
        "success": True,
        "email_sent": email_sent,
        "message": "Thanks! I'll get back to you soon."
    })

@app.route("/api/messages")
def get_messages():
    # Simple admin route — protect with a key in production
    key = request.args.get("key", "")
    if key != os.environ.get("ADMIN_KEY", "loknarayan2024"):
        return jsonify({"error": "Unauthorized"}), 401
    return jsonify(load_messages())

@app.route("/api/stats")
def stats():
    return jsonify({
        "projects": 15,
        "clients": 10,
        "experience": "2+",
        "skills": 12
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_ENV", "development") == "development"
    app.run(host="0.0.0.0", port=port, debug=debug)
