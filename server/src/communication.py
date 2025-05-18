import asyncio
import json
import struct
from mensagens.protocolo import interpretar_mensagem, criar_mensagem, mensagem_erro, mensagem_sucesso


async def read_msg(reader):
    raw_len = await reader.readexactly(4)
    msg_len = struct.unpack(">I", raw_len)[0]  # big-endian uint32
    data = await reader.readexactly(msg_len)
    return data


async def send_msg(writer, msg_bytes):
    writer.write(struct.pack(">I", len(msg_bytes)))
    writer.write(msg_bytes)
    await writer.drain()


'''async def handle_client(reader, writer):
    addr = writer.get_extra_info("peername")
    print(f"Conectado: {addr}")
    try:
        while True:
            data = await read_msg(reader)
            obj = json.loads(data.decode())
            print(f"Recebido JSON de {addr}:", obj)
            response = json.dumps(obj).encode()
            await send_msg(writer, response)
            if not data:
                break
            print(f"Recebido de {addr}: {data.decode()}")
            writer.write(data)
            await writer.drain()
    except asyncio.IncompleteReadError as e:
        print(e)
    writer.close()
    await writer.wait_closed()'''

async def handle_client(reader, writer):
    addr = writer.get_extra_info("peername")
    print(f"Conectado: {addr}")
    try:
        while True:
            data = await read_msg(reader)
            if not data:
                break

            try:
                mensagem = interpretar_mensagem(data)
                tipo = mensagem["tipo"]
                dados = mensagem["dados"]
            except Exception as e:
                erro = mensagem_erro(f"Mensagem malformada: {e}")
                await send_msg(writer, erro)
                continue

            print(f"Recebido de {addr}: {mensagem}")

            # Se for uma operação que exige autenticação (exemplo: CRIAR_LOJA)
            if tipo == "CRIAR_LOJA":
                token = dados.get("token")
                auth_result = await verificar_token_com_auth(token)

                if auth_result["tipo"] == "ERRO":
                    erro = mensagem_erro("Token inválido ou não autorizado.")
                    await send_msg(writer, erro)
                    continue

                # Aqui você pode criar a loja normalmente
                loja_nome = dados.get("nome_loja")
                print(f"Token válido. Criando loja: {loja_nome}")
                resposta = mensagem_sucesso({"mensagem": f"Loja '{loja_nome}' criada com sucesso."})
                await send_msg(writer, resposta)

            else:
                # Echo padrão para testes
                echo = mensagem_sucesso({"echo": dados})
                await send_msg(writer, echo)

    except asyncio.IncompleteReadError as e:
        print(f"Conexão encerrada por {addr}")
    except Exception as e:
        print(f"Erro inesperado: {e}")
    finally:
        writer.close()
        await writer.wait_closed()

async def verificar_token_com_auth(token: str):
    try:
        reader, writer = await asyncio.open_connection("127.0.0.1", 5000)  # IP do auth_server maquina local loopback
        msg = criar_mensagem("VERIFICAR_TOKEN", {"token": token})
        writer.write(msg)
        await writer.drain()

        data = await reader.read(2048)
        resposta = interpretar_mensagem(data)
        writer.close()
        await writer.wait_closed()
        return resposta
    except Exception as e:
        return {"tipo": "ERRO", "dados": {"motivo": str(e)}}
