FROM python:3.13-alpine

WORKDIR /app
COPY src/ ./src
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
ENV PYTHONPATH=/app

CMD ["python", "/app/src/main.py"]