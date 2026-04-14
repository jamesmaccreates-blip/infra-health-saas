FROM python:3.12-slim

# Install basic build tools just in case
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev libyaml-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Upgrade pip and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy logic
COPY . .

EXPOSE 10000
CMD ["python", "main.py"]
