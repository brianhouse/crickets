import math
import gc
import uasyncio as asyncio
import aioespnow
import bluetooth
import ubinascii
import network
from machine import Pin, PWM
from time import ticks_ms, ticks_diff, sleep_ms
from random import random, randint, choice
from config import *


STS = Pin(13, Pin.OUT)
LED = Pin(21, Pin.OUT)
PIR = Pin(33, Pin.IN)
SND = PWM(Pin(27, Pin.OUT))
SND.duty(0)


class Node():

    def __init__(self):

        # make sure Bluetooth is off
        bluetooth.BLE().active(False)

        # start wifi receiver
        self.sta = network.WLAN(network.STA_IF)
        self.sta.active(True)
        self.sta.config(txpower=POWER)
        # print(sta.config("txpower"))
        self.mac = bin_to_hex(self.sta.config('mac'))
        self.name = mac_to_name(self.mac)

        # start access point
        self.ap = network.WLAN(network.AP_IF)
        self.ap.active(True)
        self.ap.config(ssid=name_to_ssid(self.name), password="pulsecoupled", authmode=network.AUTH_WPA2_PSK)

        # activate mesh
        self.mesh = aioespnow.AIOESPNow()
        self.mesh.active(True)

        # create objects
        self.messages = []
        self.neighbors = []

        Node.current = self

    def scan(self):
        self.neighbors.clear()
        for ssid, bssid, channel, rssi, security, hidden in self.sta.scan():
            if ssid.decode('utf-8').split("_")[0] == "CK":
                self.neighbors.append(Peer.find(ssid=ssid))
        self.neighbors.sort(key=lambda n: r.rssi, reverse=True)
        return self.neighbors

    async def send(self, message):
        if not len(self.mesh.peers_table):
            return
        try:
            await self.mesh.asend(None, message, False)
        except Exception as e:
            print("Can't send", f"({e})")

    def receive(self):
        self.messages.clear()
        while True:
            sender, message = self.mesh.recv(0)
            if sender is None or message is None:
                break
            sender = Peer.find(name=sender)
            try:
                message = message.decode()
            except Exception as e:
                print(f"Received bad message ({e}) from {sender}")
            else:
                self.messages.append(sender, message)
        return self.messages


class Peer():

    seen_peers = []

    @classmethod
    def find(cls, name=None, ssid=None):
        for peer in cls.seen_peers:
            if peer.name == name or peer.ssid == ssid:
                return peer
        peer = Peer(name, ssid)
        cls.seen_peers.append(peer)
        return peer

    def __init__(self, name=None, ssid=None):
        if not name and not ssid:
            raise Exception("Peer() needs name or ssid")
        if name:
            self.name = name
            self.ssid = name_to_ssid(name)
        elif ssid:
            self.ssid = ssid
            self.name = ssid_to_name(ssid)
        self.hex_mac = name_to_mac(self.name)
        self.bin_mac = hex_to_bin(self.hex_mac)
        self.recips = 0
        print("CREATED", name)

    @property
    def rssi(self):
        try:
            return Node.current.mesh.peers_table[self.bin_mac][0]
        except KeyError:
            return None

    def __repr__(self):
        return self.name


def name_to_ssid(name):
    return f"CK_{name}".encode('utf-8')


def ssid_to_name(ssid):
    return ssid.decode("utf-8").split("_")[-1]


def name_to_mac(name):
    name = reverse(name.replace('-', '+').replace('_', '/'))
    mac_bytes = ubinascii.a2b_base64(name + '\n')
    return ':'.join(mac_bytes.hex().upper()[i:i + 2] for i in range(0, 12, 2))


def mac_to_name(mac):
    mac_bytes = bytes.fromhex(mac.replace(":", "").replace("-", ""))
    name = ubinascii.b2a_base64(mac_bytes).decode('utf-8').strip()
    return reverse(name.replace('+', '-').replace('/', '_').rstrip('\n'))


def bin_to_hex(bin_mac):
    return ubinascii.hexlify(bin_mac, ':').decode().upper()


def hex_to_bin(hex_mac):
    return ubinascii.unhexlify(hex_mac.replace(':', '').lower())


def reverse(s):
    return "".join(reversed([c for c in s]))
