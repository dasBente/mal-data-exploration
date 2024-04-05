FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY scraper.py .
COPY cronjob /etc/cron.d/cronjob

CMD ["python", "scraper.py"]