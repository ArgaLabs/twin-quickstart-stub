FROM python:3.12-slim

# Refresh inherited OS packages and pip before installing the application.
RUN apt-get update && apt-get upgrade -y && rm -rf /var/lib/apt/lists/* \
    && python -m pip install --no-cache-dir --upgrade "pip>=26.2"

COPY server.py /app/server.py
WORKDIR /app
EXPOSE 8000
CMD ["python", "server.py"]
