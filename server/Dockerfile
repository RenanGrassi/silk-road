FROM python:3.13-alpine

WORKDIR /app
COPY src/ ./src
COPY requirements.txt ./
RUN pip install -r requirements.txt
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
CMD ["python3", "-m", "src.main"]