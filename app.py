import os
import json
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Configuration: Metaclaw endpoint + token
METACLAW_URL = os.getenv("METACLAW_URL", "http://metaclaw:8000")
METACLAW_TOKEN = os.getenv("METACLAW_TOKEN", "")

# In‑memory store
hosts = {}

@app.route('/api/ping', methods=['POST'])
def ping():
    data = request.get_json() or {}
    host = data.get("host", "unknown")
    hosts[host] = {"last_ping": "just now", "data": data}
    return jsonify(success=True)

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify(hosts)

@app.route('/api/metaclaw', methods=['POST'])
def ask_metaclaw():
    payload = request.get_json() or {}
    question = payload.get("question", "")
    if not question:
        return jsonify(error="no question"), 400

    headers = {"Authorization": f"Bearer {METACLAW_TOKEN}"}
    r = requests.post(
        f"{METACLAW_URL}/v1/chat/completions",
        json={
            "model": "qwen2.5:7b-instruct-q4_K_M",
            "messages": [{"role": "user", "content": question}]
        },
        headers=headers
    )

    if r.ok:
        res = r.json()
        msg = res.get("choices", [{}])[0].get("message", {}).get("content", "")
        return jsonify(response=msg)
    else:
        return jsonify(error="metaclaw error", details=r.text), 502

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
