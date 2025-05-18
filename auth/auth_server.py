
import asyncio
from mensagens.protocolo import interpretar_mensagem, criar_mensagem, mensagem_erro, mensagem_sucesso

# Dicionário temporario no lugar de banco de dados(momentaneo)
TOKENS_VALIDOS = {
    "abc123": {"id": 1, "nome": "Renan", "email": "renan@email.com"}
}

async def handle_auth_client(reader, writer):
    try:
        data = await reader.read(2048)
        msg = interpretar_mensagem(data)
        tipo = msg["tipo"]
        dados = msg["dados"]

        if tipo == "VERIFICAR_TOKEN":
            token = dados.get("token")
            usuario = TOKENS_VALIDOS.get(token)
            if usuario:
                resposta = mensagem_sucesso({"usuario": usuario})
            else:
                resposta = mensagem_erro("Token inválido.")
        else:
            resposta = mensagem_erro("Tipo de mensagem não suportado.")

        writer.write(resposta)
        await writer.drain()

    except Exception as e:
        erro = mensagem_erro(f"Erro interno no auth: {str(e)}")
        writer.write(erro)
        await writer.drain()

    writer.close()
    await writer.wait_closed()

async def main():
    server = await asyncio.start_server(handle_auth_client, "0.0.0.0", 5000)
    addr = server.sockets[0].getsockname()
    print(f"Auth Server escutando em {addr}")
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
