import asyncio
import json
import struct


async def read_msg(reader):
    raw_len = await reader.readexactly(4)
    msg_len = struct.unpack(">I", raw_len)[0]  # big-endian uint32
    data = await reader.readexactly(msg_len)
    return data


async def send_msg(writer, msg_bytes):
    writer.write(struct.pack(">I", len(msg_bytes)))
    writer.write(msg_bytes)
    await writer.drain()


async def handle_client(reader, writer):
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
    await writer.wait_closed()
