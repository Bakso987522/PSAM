FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

ARG SUPERCRONIC_VERSION=v0.2.33
ADD https://github.com/aptible/supercronic/releases/download/${SUPERCRONIC_VERSION}/supercronic-linux-amd64 /usr/local/bin/supercronic
RUN chmod +x /usr/local/bin/supercronic

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Harmonogram z IMPORT_CRON; supercronic nie rozwija zmiennych w crontabie,
# więc plik jest generowany przy starcie kontenera.
CMD ["sh", "-c", "echo \"$IMPORT_CRON python -m importer run\" > /tmp/crontab && exec supercronic /tmp/crontab"]
