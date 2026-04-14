FROM python:3.12-slim

# 1. Build tools for C-extensions (PyYAML, etc.)
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libyaml-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 2. Install dependencies (Standard install is fine now that you have gcc)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. Copy everything (This includes main.py and skill.json)
COPY . .

# 4. Use Render's default port
EXPOSE 10000

# 5. Start the app
CMD ["python", "main.py"]
