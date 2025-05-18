FROM python:3.12-slim

WORKDIR /app
COPY src/ ./src
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update
RUN apt-get update && apt-get install -y \
    libx11-xcb1 \
    libxcb1 \
    libxcb-cursor0 \
    libxrender1 \
    libxkbcommon-x11-0 \
    libxcb-xinerama0 \
    libgl1 \
    libglib2.0-0 \
    libdbus-1-3 \
    libfontconfig1 \
    libfreetype6 \
    libxext6 \
    libxfixes3 \
    libxi6 \
    libxrandr2 \
    libxcursor1 \
    libxcomposite1 \
    libxdamage1 \
    libxtst6 \
    x11-utils \
    && rm -rf /var/lib/apt/lists/*
ENV PYTHONPATH=/app
CMD ["watchfiles", "--run", "python /app/src/main.py", "/src"]