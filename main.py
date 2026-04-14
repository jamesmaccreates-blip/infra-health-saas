import os
import requests
import smtplib
from email.message import EmailMessage
from flask import Flask, request, jsonify

app = Flask(__name__)

# --- CONFIGURATION ---
METACLAW_URL = os.getenv("METACLAW_URL", "http://localhost:11434")
METACLAW_TOKEN = os.getenv("METACLAW_TOKEN", "")
# For Gmail SMTP (using an App Password for simplicity)
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD") # App Password from Google Account
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")

def send_email_alert(ticker, signal, analysis):
    msg = EmailMessage()
    msg.set_content(analysis)
    msg['Subject'] = f"🚀 {signal} Alert: {ticker} (EaaS Sector)"
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECIPIENT_EMAIL

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
            smtp.send_message(msg)
        return True
    except Exception as e:
        print(f"Email failed: {e}")
        return False

@app.route('/api/alert', methods=['POST'])
def stock_alert_workflow():
    data = request.get_json() or {}
    ticker = data.get("ticker", "HASI")
    signal = data.get("signal", "Bullish")
    
    # 1. Get the Analysis from your EliteBook LLM
    prompt = f"Analyze {ticker} stock signal ({signal}) under the Green-Grid Subsidy Act. Focus on 2026 ROI."
    
    try:
        r = requests.post(
            f"{METACLAW_URL.rstrip('/')}/v1/chat/completions",
            json={
                "model": "qwen2.5:7b-instruct-q4_K_M",
                "messages": [{"role": "user", "content": prompt}],
                "stream": False
            },
            timeout=300
        )
        r.raise_for_status()
        analysis = r.json().get("choices", [{}])[0].get("message", {}).get("content", "")
        
        # 2. Email the Analysis
        if analysis and send_email_alert(ticker, signal, analysis):
            return jsonify(status="Success", message=f"Alert sent for {ticker}")
        
        return jsonify(status="Error", message="Analysis generated but email failed"), 500

    except Exception as e:
        return jsonify(error=str(e)), 500

# Keep your existing /api/metaclaw and /api/ping routes here...

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)