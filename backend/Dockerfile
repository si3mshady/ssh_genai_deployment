FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && pip install -r requirements.txt

COPY api /app/api

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
