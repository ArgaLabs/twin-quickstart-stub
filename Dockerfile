FROM python:3.12-slim
RUN pip install --no-cache-dir uvicorn
COPY server.py /app/server.py
WORKDIR /app
EXPOSE 8000
CMD ["python", "server.py"]
