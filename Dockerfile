FROM python:3.12-slim

COPY refresh_ensurepip.py /usr/local/bin/refresh-ensurepip.py

# Refresh inherited OS packages and pip before installing the application.
RUN apt-get update && apt-get dist-upgrade -y && rm -rf /var/lib/apt/lists/* \
    && python -m pip install --no-cache-dir --upgrade "pip>=26.2" \
    && python /usr/local/bin/refresh-ensurepip.py

COPY server.py /app/server.py
WORKDIR /app
EXPOSE 8000
CMD ["python", "server.py"]
