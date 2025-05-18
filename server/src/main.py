import asyncio
from src.utils.server_socket import SocketServer


async def main():
    server = SocketServer()
    await server.start()


if __name__ == "__main__":
    """
    Função principal para iniciar o servidor.
    """
    asyncio.run(main())
