# app.py
from flask import Flask, request, jsonify
import requests, os, json

app = Flask(__name__)

# Env vars
METACLAW_URL = os.getenv("METACLAW_URL", "http://metaclaw:8000")
METACLAW_TOKEN = os.getenv("METACLAW_TOKEN", "")

# In‑memory store for host health
hosts = {
    "localhost": {
        "last_ping": "0 minutes ago",
        "last_report": None
    }
}

@app.route('/api/ping', methods=['POST'])
def ping():
    data = request.get_json() or {}
    host = data.get("host", "unknown")
    hosts[host] = {
        "last_ping": "just now",
        "last_report": data
    }
    return jsonify(success=True)

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify(hosts)

@app.route('/api/metaclaw', methods=['POST'])
def ask_metaclaw():
    payload = request.get_json() or {}
    prompt = payload.get("question", "")
    if not prompt:
        return jsonify(error="no question"), 400

    # Forward to Metaclaw
    headers = {"Authorization": f"Bearer {METACLAW_TOKEN}"}
    r = requests.post(f"{METACLAW_URL}/v1/chat/completions", json={"model": "qwen2.5:7b-instruct-q4_K_M", "messages": [{"role": "user", "content": prompt}]}, headers=headers)
    if r.ok:
        res = r.json()
        return jsonify(response=res.get("choices", [{}])[0].get("message", {}).get("content", "")))
    else:
        return jsonify(error="metaclaw error", details=r.text), 502

if __name__ == "__main__":
    import os
    port = os.getenv('PORT', 5000)
    app.run(host='0.0.0.0', port=int(port))

@app.route("/api/stripe-webhook", methods=["POST"])
def stripe_webhook():
    payload = request.data
    with open("stripe_payloads.log", "ab") as f:
        f.write(payload)
        f.write(b"
")
    return jsonify(success=True)
