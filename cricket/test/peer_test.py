import network
import ubinascii
import math
import espnow
import bluetooth
import socket
import machine
from machine import ADC, Pin, PWM
from time import sleep, sleep_ms, ticks_ms, ticks_us
from random import random, randint, choice


print("PEER TEST")
STS = Pin(13, Pin.OUT)



def bin_to_hex(bin_mac):
    return ubinascii.hexlify(bin_mac, ':').decode().upper()


def hex_to_bin(hex_mac):
    return ubinascii.unhexlify(hex_mac.replace(':', '').lower())


def name_to_mac(name):
    # return f"7C:9E:BD:{name[:2]}:{name[2:4]}:{name[4:]}" # ?
    return f"A8:42:E3:{name[:2]}:{name[2:4]}:{name[4:]}"


def ap_to_peer(hex_mac):
    # subtract 1 from the last octet to find the peer address
    return hex_mac[:-2] + hex(int(hex_mac.split(':')[-1], 16) - 1)[-2:].upper()


global mesh, sta, ap

# make sure Bluetooth is off
bluetooth.BLE().active(False)

# start wifi receiver
sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.disconnect()

# start access point
ap = network.WLAN(network.AP_IF)
ap.active(False)
# ap.config(password='pulsecoupled', authmode=network.AUTH_WPA2_PSK)

# activate mesh
mesh = espnow.ESPNow()
mesh.active(True)

mac = sta.config('mac')
print("MAC", mac)

if mac == b'|\x9e\xbd\xd8\xea8':
    peer = b'|\x9e\xbd\xd8\xe7\xac'
else:
    peer = b'|\x9e\xbd\xd8\xea8'

mesh.add_peer(peer)
info = mesh.get_peer(peer)
print(info)

print("peer_count", mesh.peer_count())

while True:
    STS.on()
    mesh.send(peer, "hello world")
    print("-> sent message")
    STS.off()
    sender, in_message = mesh.recv(0)
    print("--> received", in_message, "from", sender)
    sleep(1)

