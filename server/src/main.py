import asyncio
from src.communication import handle_client


async def main():
    server = await asyncio.start_server(handle_client, "0.0.0.0", 65432)
    addr = server.sockets[0].getsockname()
    print(f"Escutando em {addr}")
    async with server:
        await server.serve_forever()


asyncio.run(main())
