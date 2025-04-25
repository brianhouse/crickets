import network
import ubinascii
import math
import aioespnow
import bluetooth
import socket
import machine
from machine import ADC, Pin, PWM
from time import sleep, sleep_ms, ticks_ms, ticks_us
from random import random, randint, choice
from config import *

# https://learn.adafruit.com/huzzah32-esp32-breakout-board/pinouts
STS = Pin(13, Pin.OUT)
LED = Pin(21, Pin.OUT)
PIR = Pin(33, Pin.IN)
SND = PWM(Pin(27, Pin.OUT))
SND.duty(0)


class Mesh():

    peers = []

    def __init__(self):
        global mesh, sta, ap

        # make sure Bluetooth is off
        bluetooth.BLE().active(False)

        # start wifi receiver
        self.sta = network.WLAN(network.STA_IF)
        self.sta.active(True)
        self.sta.config(txpower=POWER)
        # print(self.sta.config("txpower"))
        self.mac = bin_to_hex(self.sta.config('mac'))
        self.name = mac_to_name(self.mac)

        # start access point
        self.ap = network.WLAN(network.AP_IF)
        self.ap.active(True)
        self.ap.config(ssid=name_to_ssid(self.name), password="pulsecoupled", authmode=network.AUTH_WPA2_PSK)

        # activate mesh
        self.mesh = aioespnow.AIOESPNow()
        self.mesh.active(True)

        print(f"## {self.name} ##")

    def scan(self):
        neighbors = []
        for ssid, bssid, channel, rssi, security, hidden in self.sta.scan():
            if ssid.decode('utf-8').split("_")[0] == "CK":
                neighbors.append({'name': ssid_to_name(ssid),
                                  'rssi': rssi})
        neighbors.sort(key=lambda n: n['rssi'], reverse=True)
        return neighbors

    async def send(self, message):
        if not len(mesh.peers):
            return
        try:
            await self.mesh.asend(None, message, True)
        except Exception as e:
            print("Can't send", f"({e})")

    def receive(self):
        try:
            sender, msg = self.mesh.recv(0)
            if msg and sender:
                sender = mac_to_name(bin_to_hex(sender))
                try:
                    msg.decode()
                except Exception as e:
                    print(f"Received bad message ({e}) from {sender}")
                else:
                    return sender, msg.decode()
        except Exception as e:
            print(e)
        return None, None

    def add_peer(self, name):
        if name not in self.peers and name != self.name:
            self.mesh.add_peer(hex_to_bin(name_to_mac(name)))
            self.peers.append(name)

    def remove_peer(self, name):
        try:
            self.mesh.del_peer(hex_to_bin(name_to_mac(name)))
            self.peers.remove(name)
        except ValueError as e:
            print(e)

    def clear_peers(self):
        for peer in self.peers:
            try:
                self.mesh.del_peer(hex_to_bin(name_to_mac(peer)))
            except ValueError as e:
                print(e)
        self.peers.clear()

    def sort_peers(self):
        self.peers.sort(key=lambda peer: (self.get_rssi(peer) is None, self.get_rssi(peer)))

    def get_rssi(self, peer):
        try:
            return self.mesh.peers_table[hex_to_bin(name_to_mac(peer))][0]
        except KeyError:
            return None


def name_to_ssid(name):
    return f"CK_{name}".encode('utf-8')


def ssid_to_name(ssid):
    return ssid.decode("utf-8").split("_")[-1]


lookup_name_to_mac = {}
def name_to_mac(name):
    if name in lookup_name_to_mac:
        return lookup_name_to_mac[name]
    else:
        name = reverse(name.replace('-', '+').replace('_', '/'))
        mac_bytes = ubinascii.a2b_base64(name + '\n')
        result = ':'.join(mac_bytes.hex().upper()[i:i + 2] for i in range(0, 12, 2))
        lookup_name_to_mac[name] = result
        return result


lookup_mac_to_name = {}
def mac_to_name(mac):
    if mac in lookup_mac_to_name:
        return lookup_mac_to_name[mac]
    else:
        mac_bytes = bytes.fromhex(mac.replace(":", "").replace("-", ""))
        name = ubinascii.b2a_base64(mac_bytes).decode('utf-8').strip()
        result = reverse(name.replace('+', '-').replace('/', '_').rstrip('\n'))
        lookup_mac_to_name[mac] = result
        return result


lookup_bin_to_hex = {}
def bin_to_hex(bin_mac):
    if bin_mac in lookup_bin_to_hex:
        return lookup_bin_to_hex[bin_mac]
    else:
        result = ubinascii.hexlify(bin_mac, ':').decode().upper()
        lookup_bin_to_hex[bin_mac] = result
        return result


lookup_hex_to_bin = {}
def hex_to_bin(hex_mac):
    if hex_mac in lookup_hex_to_bin:
        return lookup_hex_to_bin[hex_mac]
    else:
        result = ubinascii.unhexlify(hex_mac.replace(':', '').lower())
        lookup_hex_to_bin[hex_mac] = result
        return result


def map(value, in_min, in_max, out_min, out_max):
    value = (value - in_min) / float(in_max - in_min)
    return (value * (out_max - out_min)) + out_min


def reverse(s):
    return "".join(reversed([c for c in s]))


mesh = Mesh()
