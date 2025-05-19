import asyncio
import json


class SocketClient:
    def __init__(self, host="silk-road-server", port=65432):
        self.host = host
        self.port = port
        self.reader = None
        self.writer = None

    async def connect(self):
        self.reader, self.writer = await asyncio.open_connection(self.host, self.port)
        print("Conectado ao servidor.")

    async def send(self, data):
        encoded = json.dumps(data).encode()
        self.writer.write(len(encoded).to_bytes(4, "big") + encoded)
        await self.writer.drain()

    async def receive(self):
        try:
            raw_len = await self.reader.readexactly(4)
            msg_len = int.from_bytes(raw_len, "big")
            data = await self.reader.readexactly(msg_len)
            return json.loads(data.decode())
        except asyncio.IncompleteReadError:
            print("Conexão perdida.")
            return None

    async def close(self):
        self.writer.close()
        await self.writer.wait_closed()
        print("Conexão encerrada.")
