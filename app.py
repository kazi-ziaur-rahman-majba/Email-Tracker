from flask import Flask, request, send_file, render_template, jsonify
import sqlite3
import io
import base64
import datetime
import requests

app = Flask(__name__)
DB = "tracker.db"

PIXEL = base64.b64decode(
    "R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"
)

def init_db():
    with sqlite3.connect(DB) as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS opens (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                sender      TEXT,
                receiver    TEXT,
                subject     TEXT,
                opened_at   TEXT NOT NULL,
                ip          TEXT,
                country     TEXT,
                city        TEXT,
                device      TEXT
            )
        """)
        con.commit()

def get_location(ip):
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}", timeout=3)
        data = r.json()
        if data.get("status") == "success":
            return data.get("country", "Unknown"), data.get("city", "Unknown")
    except:
        pass
    return "Unknown", "Unknown"

def get_device(user_agent):
    ua = user_agent.lower()
    if "mobile" in ua or "android" in ua or "iphone" in ua:
        return "Mobile"
    elif "tablet" in ua or "ipad" in ua:
        return "Tablet"
    else:
        return "Desktop"

# /track?sender=a@gmail.com&receiver=b@gmail.com&subject=Hello
@app.route("/track")
def track():
    sender   = request.args.get("sender", "Unknown")
    receiver = request.args.get("receiver", "Unknown")
    subject  = request.args.get("subject", "")

    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    if ip and "," in ip:
        ip = ip.split(",")[0].strip()

    user_agent = request.headers.get("User-Agent", "")
    device = get_device(user_agent)
    country, city = get_location(ip)
    opened_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with sqlite3.connect(DB) as con:
        con.execute(
            "INSERT INTO opens (sender, receiver, subject, opened_at, ip, country, city, device) VALUES (?,?,?,?,?,?,?,?)",
            (sender, receiver, subject, opened_at, ip, country, city, device)
        )
        con.commit()

    return send_file(io.BytesIO(PIXEL), mimetype="image/gif")

@app.route("/")
def dashboard():
    return render_template("dashboard.html")

@app.route("/api/stats")
def stats():
    with sqlite3.connect(DB) as con:
        con.row_factory = sqlite3.Row
        rows = con.execute(
            "SELECT * FROM opens ORDER BY opened_at DESC"
        ).fetchall()
    return jsonify([dict(r) for r in rows])

@app.route("/api/emails")
def emails():
    with sqlite3.connect(DB) as con:
        con.row_factory = sqlite3.Row
        rows = con.execute("""
            SELECT sender, receiver, subject,
                   COUNT(*) as open_count,
                   MIN(opened_at) as first_open,
                   MAX(opened_at) as last_open
            FROM opens
            GROUP BY sender, receiver, subject
            ORDER BY last_open DESC
        """).fetchall()
    return jsonify([dict(r) for r in rows])

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
