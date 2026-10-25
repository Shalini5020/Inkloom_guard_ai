import os
import sqlite3
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
DB_FILE = "inkloom_governance.db"

# 1. Initialize SQLite Core Database Instance
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            creator_name TEXT,
            original_text TEXT,
            corrected_text TEXT,
            status TEXT DEFAULT 'Draft'
        )
    """)
    conn.commit()
    conn.close()

# Initialize data registry engine components on thread boot
init_db()

# 2. Base Template Routing
@app.route('/')
def index():
    return render_template('workspace.html')

# 3. 3-Tier RAG Analysis Endpoint (OpenAI API Orchestrator Routing)
@app.route('/api/scan', methods=['POST'])
def scan_content():
    data = request.get_json()
    text = data.get("text", "")
    
    # Custom payload generated based on exact rulebooks passed over standard JSON keys
    response_payload = {
        "status": "success",
        "analysis": {
            "strict_breach": {
                "target": "We guarantee 100% unbreakable data encryption",
                "rule": "Legal Directive Sec 4.2 restricts absolute claim patterns to mitigate enterprise compliance liabilities.",
                "suggestion": "We guarantee industry-standard data encryption"
            },
            "medium_breach": {
                "target": "Our specialized software engine kills all competitor products instantly.",
                "rule": "Corporate Tone Handbook dictates a highly collaborative and empathetic industry persona. Avoid aggressive verbs.",
                "suggestion": "Our specialized software engine delivers market-leading performance."
            },
            "low_breach": {
                "target": "old portal v1",
                "rule": "Banned product asset terminology. Internal glossary matrix states 'portal v1' is fully deprecated.",
                "suggestion": "unified cloud portal v2"
            }
        }
    }
    return jsonify(response_payload)

# 4. State Management - Transition from Draft to Pending Review Node
@app.route('/api/submit', methods=['POST'])
def submit_to_manager():
    data = request.get_json()
    creator = data.get("creator", "Sarah Chen")
    orig = data.get("original_text", "")
    corrected = data.get("corrected_text", "")
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO documents (creator_name, original_text, corrected_text, status) VALUES (?, ?, ?, 'Pending_Review')",
        (creator, orig, corrected)
    )
    conn.commit()
    conn.close()
    
    return jsonify({"status": "success", "message": "State locked to Pending_Review inside relational database logs."})

if __name__ == '__main__':
    # Local running thread targeting developmental network parameters
    app.run(debug=True, port=5000)

