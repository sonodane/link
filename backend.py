from flask import Flask, request, jsonify
from datetime import datetime
import json
import os

app = Flask(__name__)
LOG_FILE = 'analytics_log.json'

# Ensure the log file exists
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, 'w') as f:
        json.dump([], f)

@app.route('/track', methods=['POST'])
def track():
    data = request.get_json()
    entry = {
        'link': data.get('link'),
        'timestamp': data.get('timestamp', datetime.utcnow().isoformat())
    }
    
    with open(LOG_FILE, 'r+') as f:
        logs = json.load(f)
        logs.append(entry)
        f.seek(0)
        json.dump(logs, f, indent=2)

    return jsonify({"status": "success", "message": "Link tracked."}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
