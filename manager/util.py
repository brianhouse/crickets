import network, espnow, bluetooth, usocket
from time import sleep

STATUS_CODES = {200: 'BEACON_TIMEOUT',
                201: 'NO_AP_FOUND',
                202: 'WRONG_PASSWORD',
                203: 'ASSOC_FAIL',
                204: 'HANDSHAKE_TIMEOUT',
                1000: 'IDLE',
                1001: 'CONNECTING',
                1010: 'GOT_IP'
                }


bluetooth.BLE().active(False)
espnow.ESPNow().active(False)
network.WLAN(network.AP_IF).active(False)

sta = network.WLAN(network.STA_IF)
sta.active(True)


def scan():
    neighbors = []
    for ssid, bssid, channel, rssi, security, hidden in sta.scan():
        if ssid.decode('utf-8').split("_")[0] == "ESP":
            neighbors.append({'name': ssid.decode("utf-8").split("_")[-1],
                              'rssi': rssi}
                             )
    neighbors.sort(key=lambda n: n['rssi'], reverse=True)
    return neighbors


def connect(ssid):
    sta.disconnect()
    sleep(.5)
    print(f"Connecting to {ssid}...")
    sta.connect(ssid, "pulsecoupled")
    while not sta.isconnected():
        status = sta.status()
        if status in STATUS_CODES:
            print(STATUS_CODES[status])
        else:
            print(".")
        sleep(1)
    print("--> connected")


def request(url):
    if not sta.isconnected():
        sta.connect()
    url = url.replace("http://", "").replace("https://", "")
    host = url.split("/")[0]
    path = url.replace(host, "")
    port = 80
    print("Request", host, path, port)
    addr_info = usocket.getaddrinfo(host, port)[0][-1]
    s = usocket.socket()
    s.connect(addr_info)
    s.send(f"GET {path} HTTP/1.1\r\nHost: 192.168.4.1\r\nConnection: close\r\n\r\n".encode())
    response = b""
    while True:
        data = s.recv(1024)
        if not data:
            break
        response += data
    s.close()
    body = response.split(b"\r\n\r\n", 1)[-1]
    return body.decode('utf-8')


def post_file(url, filename, filedata):
    url = url.replace("http://", "").replace("https://", "")
    host = url.split("/")[0]
    path = url.replace(host, "")
    port = 80
    print(host, path, port)
    addr_info = usocket.getaddrinfo(host, port)[0][-1]
    s = usocket.socket()
    s.connect(addr_info)
    # Create a boundary for multipart data
    boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
    body = "\r\n".join((
        f"--{boundary}",
        f"Content-Disposition: form-data; name=\"file\"; filename=\"{filename}\"",
        "Content-Type: application/octet-stream",
        "\r\n",
    )).encode() + filedata + f"\r\n--{boundary}--\r\n".encode()
    headers = "\r\n".join((
        f"POST {path} HTTP/1.1",
        f"Host: {host}",
        f"Content-Type: multipart/form-data; boundary={boundary}",
        f"Content-Length: {len(body)}",
        "Connection: close",
        "\r\n"
    ))
    s.send(headers.encode() + body)
    response = b""
    while True:
        data = s.recv(1024)
        if not data:
            break
        response += data
    s.close()
    body = response.split(b"\r\n\r\n", 1)[-1]
    return body.decode('utf-8')
