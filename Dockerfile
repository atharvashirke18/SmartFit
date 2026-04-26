FROM python:3.11-slim

WORKDIR /app

# Avoid creating .pyc files and force unbuffered logs.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install dependencies first for better layer caching.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source.
COPY . .

# Railway provides PORT at runtime; Flask app reads it.
EXPOSE 8080

CMD ["python", "app.py"]
