FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
  libx11-xcb1 \
  libxcb-icccm4 \
  libxcb-image0 \
  libxcb-keysyms1 \
  libxcb-randr0 \
  libxcb-render-util0 \
  libxcb-shape0 \
  libxcb-xkb1 \
  libxkbcommon-x11-0 \
  libxcb-cursor0 \
  libqt6gui6 \
  libqt6widgets6 \
  libqt6core6 \
  x11-utils \
  --no-install-recommends && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/*

ENV QT_X11_NO_MITSHM=1
ENV DISPLAY=:0
WORKDIR /app

COPY requirements.txt .
COPY src/ ./src
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --no-cache-dir -r requirements.txt
RUN ls 
RUN chmod +x src/main.py
ENV PYTHONPATH=/app
CMD ["python", "src/main.py"] 









# FROM ubuntu:22.04

# # Seta variáveis para rodar o PyQt6
# ENV DEBIAN_FRONTEND=noninteractive
# ENV QT_QPA_PLATFORM=xcb

# # Instala dependências do PyQt6
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     xvfb x11-utils x11vnc fluxbox \
#     curl wget unzip \
#     libegl1 libgl1 libx11-xcb1 libxcb1 libxcb-cursor0 \
#     libxcb-util1 libxcb-icccm4 libxcb-image0 libxcb-keysyms1 \
#     libxcb-render0 libxcb-render-util0 libxcb-shape0 libxcb-shm0 \
#     libxcb-sync1 libxcb-xfixes0 libxcb-xinerama0 libxcb-randr0 \
#     libxrender1 libxext6 libxi6 libxcomposite1 libxdamage1 libxrandr2 \
#     libxcursor1 libxkbcommon-x11-0 libxfixes3 libglib2.0-0 libfontconfig1 \
#     libfreetype6 libdbus-1-3 libxtst6 \
#     qt6-base-dev qt6-base-dev-tools qtwayland5 \
#     && rm -rf /var/lib/apt/lists/*

# # Instala o Python 3.12
# RUN apt-get update && apt-get install -y software-properties-common && \
#     add-apt-repository ppa:deadsnakes/ppa && \
#     apt-get update && apt-get install -y python3.12 python3.12-dev python3.12-venv && \
#     rm -rf /var/lib/apt/lists/*

# # Usa python3.12 como default
# RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.12 1
# # Instala pip e pipenv
# RUN python3 -m ensurepip && pip3 install --no-cache-dir --upgrade pip pipenv

# # Cria um ambiente virtual
# RUN python3.12 -m venv /venv
# ENV PATH="/venv/bin:$PATH"
# # Atualiza o pip
# RUN pip install --no-cache-dir --upgrade pip
# # Instala o pipenv
# RUN pip install --no-cache-dir pipenv

# # Instala dependências do python
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     build-essential libssl-dev libffi-dev python3-dev \
#     && rm -rf /var/lib/apt/lists/*

# # Instala noVNC -> Pior coisa que fiz
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     git python3-websockify \
#     && git clone https://github.com/novnc/noVNC.git /opt/novnc \
#     && ln -s /opt/novnc/vnc.html /opt/novnc/index.html

# # Copia a aplicação
# COPY src/ /app
# COPY entrypoint.sh /entrypoint.sh
# RUN chmod +x /entrypoint.sh
# WORKDIR /app
# COPY requirements.txt ./

# # Instala dependências do pip
# RUN pip install -r requirements.txt

# # Usa o entrypoint para iniciar Xvfb e o app
# EXPOSE 6080 5900
# ENTRYPOINT ["/entrypoint.sh"]
# ENV PYTHONPATH=/app
# CMD ["python3", "/app/src/main.py"]