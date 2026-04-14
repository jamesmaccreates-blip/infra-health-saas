import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Configuration: METACLAW_URL should be your ngrok address
METACLAW_URL = os.getenv("METACLAW_URL", "http://localhost:11434")
METACLAW_TOKEN = os.getenv("METACLAW_TOKEN", "")

# Simple in-memory store for the /api/ping and /api/health routes
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
        return jsonify(error="no question provided"), 400

    headers = {
        "Authorization": f"Bearer {METACLAW_TOKEN}",
        "Content-Type": "application/json"
    }

    try:
        # Standardize the URL to the Ollama OpenAI-compatible endpoint
        base_url = METACLAW_URL.rstrip('/')
        endpoint = f"{base_url}/v1/chat/completions"

        # Construct the request for Qwen 2.5
        r = requests.post(
            endpoint,
            json={
                "model": "qwen2.5:7b-instruct-q4_K_M",
                "messages": [{"role": "user", "content": question}],
                "stream": False  # Prevents Render from timing out while waiting for chunks
            },
            headers=headers,
            timeout=300  # Give your EliteBook 90 seconds to process the inference
        )
        
        r.raise_for_status()
        res = r.json()
        
        # Safely extract the AI's response
        choices = res.get("choices", [])
        if choices:
            msg = choices[0].get("message", {}).get("content", "")
            return jsonify(response=msg)
        
        return jsonify(error="empty response from model"), 500

    except requests.exceptions.RequestException as e:
        # This will reveal if ngrok is down or if the connection is being refused
        return jsonify(error="connection to local AI failed", details=str(e)), 502

if __name__ == "__main__":
    # Render provides the PORT environment variable automatically
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)