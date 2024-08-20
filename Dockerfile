FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -U pip setuptools wheel; pip install --no-cache-dir -r requirements.txt

CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT}"]
