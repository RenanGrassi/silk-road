#!/bin/bash
set -e

echo "[INFO] Iniciando Xvfb..."
Xvfb :99 -screen 0 1024x768x16 &
XVFB_PID=$!

# Espera até o Xvfb estar pronto
for i in {1..50}; do
    xdpyinfo -display :99 > /dev/null 2>&1 && break
    echo "[entrypoint] Waiting for Xvfb..."
    sleep 1
done

echo "[INFO] Iniciando Fluxbox..."
fluxbox &

echo "[INFO] Iniciando x11vnc..."
x11vnc -display :99 -nopw -forever -shared &

echo "[INFO] Iniciando noVNC..."
websockify --web=/opt/novnc 6080 localhost:5900 &

# Aqui seta DISPLAY=:99 para o app
export DISPLAY=:99
echo "[INFO] DISPLAY set to $DISPLAY"

echo "[INFO] Executando aplicação: $@"
exec env DISPLAY=$DISPLAY "$@"