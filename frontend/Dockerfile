FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && pip install -r requirements.txt

COPY frontend /app/frontend

CMD ["streamlit", "run", "frontend/dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]
