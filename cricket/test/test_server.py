import socket

PORT = 8088

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(("0.0.0.0", PORT))
server.listen(1)
print(f"Listening on port {PORT}")
print()

while True:
    try:
        client, address = server.accept()
        print(f"Connection from {address[0]}...")
        client.settimeout(1)
        request = client.recv(1024).decode()
        headers = request.split('\n')
        page = headers[0].split()[1] if len(headers) > 0 else "/"
        print(f"Returning \"{page}\"...")
        content = "HELLO WORLD"
        print(content)
        content += "\r\n"
        content_length = len(content)
        response = (
            "HTTP/1.0 200 OK\r\n",
            "Content-Type: text/plain\r\n",
            f"Content-Length: {content_length}\r\n",
            "\r\n",
            f"{content}"
        )
        client.sendall("".join(response).encode())
        client.close()
        print("--> done")
    except Exception as e:
        print(f"--> error: {e}")
        client.close()
    print()

server.close()

