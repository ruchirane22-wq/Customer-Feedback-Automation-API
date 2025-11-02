from flask import Flask, request, jsonify, g
import uuid
import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), 'feedback.db')

app = Flask(__name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DB_PATH)
        db.row_factory = sqlite3.Row
    return db

def init_db():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS feedback_links (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cust_sr_no TEXT NOT NULL,
        cust_mob_no TEXT NOT NULL,
        cust_veh_no TEXT NOT NULL,
        feedback_id TEXT NOT NULL,
        link TEXT NOT NULL,
        created_at TEXT NOT NULL
    )""")
    db.commit()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.before_first_request
def setup():
    # ensure folder exists and DB initialized
    init_db()

@app.route('/create-feedback-link', methods=['POST'])
def create_feedback_link():
    data = request.get_json(force=True, silent=True)
    if not data:
        return jsonify({"error": "Invalid or missing JSON payload"}), 400

    cust_sr_no = data.get("cust_sr_no")
    cust_mob_no = data.get("cust_mob_no")
    cust_veh_no = data.get("cust_veh_no")

    # Basic validation
    if not all([cust_sr_no, cust_mob_no, cust_veh_no]):
        return jsonify({"error": "Missing required fields: cust_sr_no, cust_mob_no, cust_veh_no"}), 400

    # Generate a short unique id and link
    feedback_id = uuid.uuid4().hex[:10]
    domain = "tatamotors.com"
    feedback_link = f"https://feedback.{domain}/feedback/{feedback_id}"

    created_at = datetime.utcnow().isoformat() + 'Z'

    # Save to SQLite
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO feedback_links (cust_sr_no, cust_mob_no, cust_veh_no, feedback_id, link, created_at) VALUES (?, ?, ?, ?, ?, ?)",
        (cust_sr_no, cust_mob_no, cust_veh_no, feedback_id, feedback_link, created_at)
    )
    db.commit()

    return jsonify({
        "cust_sr_no": cust_sr_no,
        "cust_mob_no": cust_mob_no,
        "cust_veh_no": cust_veh_no,
        "link": feedback_link,
        "feedback_id": feedback_id,
        "created_at": created_at
    }), 200

@app.route('/links', methods=['GET'])
def list_links():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT id, cust_sr_no, cust_mob_no, cust_veh_no, feedback_id, link, created_at FROM feedback_links ORDER BY id DESC LIMIT 100")
    rows = cursor.fetchall()
    result = [dict(r) for r in rows]
    return jsonify(result), 200

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status":"ok"}), 200

if __name__ == '__main__':
    # create DB if not exists
    if not os.path.exists(DB_PATH):
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    app.run(host='0.0.0.0', port=5000, debug=True)
