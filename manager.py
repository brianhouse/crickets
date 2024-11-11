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
    if sta.isconnected():
        sta.disconnect()
    print(f"Connecting to {ssid.decode('utf-8')}...")
    try:
        sta.connect(ssid, "pulsecoupled")
    except Exception as e:
        print(e)
    while not sta.isconnected():
        status = sta.status()
        if status in STATUS_CODES:
            print(STATUS_CODES[status])
        else:
            print(".")
        sleep(1)
    print("--> connected")


def request(url):
    print(f"Requesting {url}...")
    url = url.replace("http://", "").replace("https://", "")
    host = url.split("/")[0]
    path = url.replace(host, "")
    port = 80
    print(host, path, port)
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


while True:
    neighbors = scan()
    print("CRICKETS:")
    print(neighbors)
    for neighbor in neighbors:
        connect(f"ESP_{neighbor['name']}".encode('utf-8'))
        print(sta.isconnected())
        try:
            response = request("http://192.168.4.1/")
            print(response)
        except Exception as e:
            print("Request failed:", e)
        sleep(1)
        print()
    print()
    sleep(5)
