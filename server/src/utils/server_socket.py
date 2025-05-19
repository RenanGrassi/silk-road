import asyncio
import json
import struct
from src.utils.find_route import RouteRequests
from src.abstracts.base_request import BaseDTO


class SocketServer:
    def __init__(self, host="0.0.0.0", port=65432):
        self.host = host
        self.port = port
        self.server = None
        self.router = RouteRequests()

    async def start(self):
        self.server = await asyncio.start_server(
            self.handle_client, self.host, self.port
        )
        addr = self.server.sockets[0].getsockname()
        print(f"Escutando em {addr}")
        async with self.server:
            await self.server.serve_forever()

    async def stop(self):
        if self.server:
            self.server.close()
            await self.server.wait_closed()
            print("Servidor encerrado.")
        else:
            print("Servidor não está em execução.")

    async def handle_client(self, reader, writer):
        try:
            while True:
                data = await self.read_msg(reader)
                try:
                    decoded = json.loads(data.decode())
                    if type(decoded) is str:
                        print(f"Recebido: {decoded}, {type(decoded)}")
                        decoded = json.loads(decoded)
                    print(f"Recebido: {decoded}, {type(decoded)}")
                    if not decoded.get("group") and not decoded.get("route"):
                        await self.send_error("Grupo ou rota não encontrados", writer)
                        continue
                except json.JSONDecodeError as e:
                    print(f"Erro ao decodificar JSON: {e}")
                    await self.send_error("Erro ao decodificar JSON", writer)
                    continue
                dto = BaseDTO(**decoded)
                try:
                    response = self.router.find_route(dto)
                    await self.send_success(
                        {"type": "SUCCESS", "data": response}, writer
                    )
                except Exception as e:
                    await self.send_error(e.__str__(), writer)
                    continue
        except asyncio.IncompleteReadError as e:
            print(e)
        writer.close()
        await writer.wait_closed()

    async def read_msg(self, reader):
        raw_len = await reader.readexactly(4)
        msg_len = struct.unpack(">I", raw_len)[0]  # big-endian uint32
        data = await reader.readexactly(msg_len)
        return data

    async def send_success(self, message: dict, writer):
        success_message = {"type": "SUCCESS", "data": message}
        return await self.send_message(writer, json.dumps(success_message).encode())

    async def send_error(self, message: str, writer):
        error_message = {"type": "ERROR", "data": {"clasure": message}}
        return await self.send_message(writer, json.dumps(error_message).encode())

    async def send_message(self, writer, msg_bytes):
        writer.write(struct.pack(">I", len(msg_bytes)))
        writer.write(msg_bytes)
        await writer.drain()
