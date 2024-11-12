import socket, time
from esp_helper import *
from config import *


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def start_http():
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("0.0.0.0", HTTP))
    server.listen(1)
    print(f"Listening on port {HTTP}")
    print()


def check_http():
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


start_http()

# scan for neighbors, sort by reverse signal strength
print("Looking for neighbors...")
clear_peers()
neighbors = scan()
neighbors.sort(key=lambda n: n['rssi'], reverse=True)
count = 0
for neighbor in neighbors:
    if neighbor['ssid'].split("_")[0] == "ESP" and \
            neighbor['rssi'] > RANGE:
        mac = ap_to_peer(neighbor['mac'])
        print(neighbor['rssi'], neighbor['ssid'], mac)
        add_peer(mac)
        count += 1
        if count == HOOD:
            break
print("--> done")

while True:
    print(time.time())
    check_http()
    print(time.time())

