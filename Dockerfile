FROM python:3.12-slim

COPY requirements.txt .

RUN apt-get update && apt-get install -y \
    libpq-dev gcc && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app

COPY /CafeBooking/ .