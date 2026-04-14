FROM python:3.12-slim

# 1. Install required build tools (Your stashed changes)
# This prevents the "PyYAML" build errors by providing a compiler
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libyaml-dev && \
    rm -rf /var/lib/apt/lists/*

# 2. Set the working directory
WORKDIR /app

# 3. Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy your new code (including main.py and skill.json)
COPY . .

# 5. Render expects port 5000 by default for web services
EXPOSE 5000

# 6. Run your new entry point
CMD ["python", "main.py"]
