import network, ubinascii, time
from urequests import get, post


def bin_to_hex(bin_mac):
    return ubinascii.hexlify(bin_mac, ':').decode().upper()


def ap_to_peer(hex_mac):
    # subtract 1 from the last octet to find the peer address
    return hex_mac[:-2] + hex(int(hex_mac.split(':')[-1], 16) - 1)[-2:].upper()


def connect(ssid, pw):
    try:
        if not sta.isconnected():
            print("Connecting to network...")
            try:
                sta.connect(ssid, pw)
            except Exception as e:
                print(e)
            while not sta.isconnected():
                print("...not connected")
                time.sleep(1)
        print("Connected!:", sta.ifconfig())
    except NameError as e:
        print(e)
        print("Wifi not started")


def scan():
    global sta
    nets = []
    for ssid, bssid, channel, rssi, security, hidden in sta.scan():
        nets.append({'ssid': ssid.decode("utf-8"),
                     'mac': bin_to_hex(bssid),
                     'channel': channel,
                     'rssi': rssi,
                     'security': security,
                     'hidden': hidden
                     })
    return nets


sta = network.WLAN(network.STA_IF)
sta.active(True)
print("MAC address is", bin_to_hex(sta.config('mac')))

while True:
    nets = scan()
    print("CRICKETS:")
    for net in nets:
        if net['ssid'].split("_")[0] == "ESP":
            mac = ap_to_peer(net['mac'])
            print(net['ssid'], mac)
            connect(net['ssid'], '')
            #r = get("http://192.168.4.1:8088/peers")
            #print(r.text)
            time.sleep(1)
    print()


