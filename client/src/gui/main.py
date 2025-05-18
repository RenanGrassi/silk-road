from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QTextEdit,
    QLineEdit,
    QPushButton,
)
from PySide6.QtCore import QTimer
import asyncio
import sys
from src.utils.client_socket import SocketClient


class ClientGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Silk Road Client")
        self.resize(400, 300)

        self.layout = QVBoxLayout()
        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)
        self.layout.addWidget(self.text_area)

        self.input_line = QLineEdit()
        self.layout.addWidget(self.input_line)

        self.send_button = QPushButton("Enviar")
        self.send_button.clicked.connect(self.send_message)
        self.layout.addWidget(self.send_button)

        self.setLayout(self.layout)

        self.client = SocketClient()
        self.loop = asyncio.get_event_loop()
        self.loop.create_task(self.start_client())

        self.timer = QTimer()
        self.timer.timeout.connect(self.process_events)
        self.timer.start(50)  # roda o loop do asyncio com frequência

    def process_events(self):
        self.loop.call_soon(self.loop.stop)
        self.loop.run_forever()

    async def start_client(self):
        await self.client.connect()
        self.text_area.append("Conectado ao servidor!")
        while True:
            response = await self.client.receive()
            if response is None:
                self.text_area.append("Servidor desconectado.")
                break
            self.text_area.append(f"Servidor: {response}")

    def send_message(self):
        msg = self.input_line.text()
        self.input_line.clear()
        self.loop.create_task(self.client.send({"msg": msg}))
