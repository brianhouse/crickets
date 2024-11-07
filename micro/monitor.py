import uasyncio as asyncio
import ujson, socket
from config import *


async def handle_request(reader, writer):
    request = await reader.read(1024)
    request = request.decode('utf-8')
    headers = request.split('\n')
    page = headers[0].split()[1] if len(headers) > 0 else "/"
    print("Request received:", headers, page)
    if page == "/peers":
        content = str(peers)
    else:
        content = "HELLO WORLD"
    content += "\r\n"
    headers = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(content)}\r\n\r\n"
    writer.write(headers.encode())
    writer.write(content.encode())
    await writer.drain()
    await writer.wait_closed()


async def start_server():
    await asyncio.start_server(handle_request, "0.0.0.0", HTTP)
    print(f"Server running on port {HTTP}")
    try:
        while True:
            await asyncio.sleep(3600)
    except asyncio.CancelledError:
        pass


asyncio.run(start_server())