#!/bin/bash
set -e

# Inicia servidor gráfico virtual
Xvfb :1 -screen 0 1024x768x16 &

# Inicia uma sessão com window manager leve (fluxbox)
fluxbox &

# Inicia o servidor VNC apontando para o Xvfb
x11vnc -display :1 -nopw -forever -shared -rfbport 5900 &

# Inicia o servidor web noVNC (porta 6080 por padrão)
websockify --web=/opt/novnc 6080 localhost:5900 &

# Espera um pouco e inicia sua app
sleep 2
exec "$@"