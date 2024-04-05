FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY scraper.py .

RUN export SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt
CMD ["python", "-u", "scraper.py"]