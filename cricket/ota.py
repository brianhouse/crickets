import uasyncio as asyncio
import ujson, socket, re
from config import *


async def handle_request(reader, writer):
    reset = False
    request = await reader.read(1024)
    request = request.decode('utf-8')
    print(request)
    headers = request.split('\r\n')
    page = headers[0].split()[1] if len(headers) > 0 else "/"
    if page == "/peers":
        content = f"{mesh.name} {mesh.peers}"
    elif page == "/reset":
        content = "resetting"
        reset = True
        machine.reset()
    elif page == "/file":
        content = "NO FILE DATA"
        for header in headers:
            if header.startswith("Content-Type:"):
                if "boundary=" in header:
                    boundary_start = header.find("boundary=") + len("boundary=")
                    boundary = header[boundary_start:].strip()
                    file_data, filename = await extract_file(request, boundary)
                    if file_data:
                        with open(f"/{filename}", 'wb') as f:
                            f.write(file_data)
                            content = "SUCCESS"
    else:
        content = "HELLO WORLD"
    headers = ("HTTP/1.1 200 OK",
               "Content-Type: text/plain; charset=utf-8",
               f"Content-Length: {len(content)}",
               "\r\n"
               )
    writer.write("\r\n".join(headers).encode('utf-8'))
    writer.write(content.encode('utf-8'))
    await writer.drain()
    await writer.wait_closed()
    if reset:
        machine.reset()


async def extract_file(request, boundary):
    parts = request.split(f"--{boundary}")
    for part in parts:
        if 'Content-Disposition' in part and 'filename' in part:
            match = re.search(r'filename="([^"]+)"', part)
            if match:
                filename = match.group(1)
            else:
                filename = "uploaded_file"
            file_start = part.find('\r\n\r\n') + 4
            file_data = part[file_start:]
            return file_data, filename
    return None, None


async def start_ota():
    await asyncio.start_server(handle_request, "0.0.0.0", 80)
    print(f"Server running")
    try:
        while True:
            await asyncio.sleep(3600)
    except asyncio.CancelledError:
        pass


