from flask import Flask, request, jsonify, render_template_string
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

@app.route('/analytics')
def analytics():
    with open(LOG_FILE, 'r') as f:
        logs = json.load(f)

    counts = {}
    for log in logs:
        link = log['link']
        counts[link] = counts.get(link, 0) + 1

    html = '''
    <html>
      <head>
        <title>Analytics Dashboard</title>
        <style>
          body { font-family: sans-serif; background: #121212; color: #eee; padding: 20px; }
          h1 { color: #0ff; }
          .link-data { margin-bottom: 10px; }
        </style>
      </head>
      <body>
        <h1>🔍 Analytics Dashboard</h1>
        {% for link, count in counts.items() %}
          <div class="link-data">🔗 <strong>{{ link }}</strong>: {{ count }} click{{ 's' if count > 1 else '' }}</div>
        {% endfor %}
      </body>
    </html>
    '''
    return render_template_string(html, counts=counts)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
