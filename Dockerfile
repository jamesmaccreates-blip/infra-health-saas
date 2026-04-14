# Use the more feature‑rich image or keep slim and use wheels
FROM python:3.12-slim  # or change to python:3.12

WORKDIR /app

# Copy requirements first to leverage cache
COPY requirements.txt .

# Install only the required wheels, avoid building PyYAML
RUN pip install --no-cache-dir --no-binary :all: -r requirements.txt

# Copy the app code
COPY app.py .

EXPOSE 5000
CMD ["python", "app.py"]
