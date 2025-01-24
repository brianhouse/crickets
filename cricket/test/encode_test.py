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
print("mac", mac)

hex_mac = bin_to_hex(mac)
print("hex mac", hex_mac)

bin_mac = hex_to_bin(hex_mac)
print("bin_mac", bin_mac)

assert mac == bin_mac


ssid = ap.config('essid')
name = ssid.split("_")[-1]
print("name", name)
name_mac = name_to_mac(name)
print(name_mac)
assert name_mac == hex_mac

name_bin_mac = hex_to_bin(name_mac)
assert name_bin_mac == bin_mac

# print(f"## {name} ##")



