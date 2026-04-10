# Dockerfile
# Build optimized Python Flask microservice
# Base image key for Metaclaw integration
FROM python:3.12-slim

# Install Metaclaw local runtime (via pip install) or pull the local docker image
# But we’ll just expose an endpoint to a local Metaclaw container via environment

# Set workdir
WORKDIR /app

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY app.py .

# Expose port for Flask
EXPOSE 5000

# Set entrypoint
CMD ["python", "app.py"]
