import math
import gc
import uasyncio as asyncio
import espnow
import bluetooth
import ubinascii
import network
import ujson as json
from machine import Pin, PWM, DAC, reset
from time import ticks_ms, ticks_diff, sleep_ms
from random import random, randint, choice, randrange
from config import *


STS = Pin(13, Pin.OUT)
LED = Pin(21, Pin.OUT)
PIR = Pin(33, Pin.IN)
try:
    ALG = DAC(Pin(25))
except Exception:
    reset()
SND = PWM(Pin(27, Pin.OUT))
SND.duty(0)

try:
    with open("topo.json", 'r') as f:
        topo = json.loads(f.read())
except Exception as e:
    print("Error loading topo:", e)


class Node():

    def __init__(self):

        # make sure Bluetooth is off
        bluetooth.BLE().active(False)

        # start wifi receiver
        self.sta = network.WLAN(network.STA_IF)
        self.sta.active(True)
        self.mac = bin_to_hex(self.sta.config('mac'))
        self.name = mac_to_name(self.mac)
        self.channel = find_channel(self.name)

        # start access point
        self.ap = network.WLAN(network.AP_IF)
        self.ap.active(True)
        self.ap.config(ssid=name_to_ssid(self.name),
                       password="pulsecoupled",
                       authmode=network.AUTH_WPA2_PSK,
                       txpower=POWER,
                       channel=self.channel)
        # print(self.ap.config("txpower"))

        # activate mesh
        self.mesh = espnow.ESPNow()
        self.mesh.active(True)
        self.mesh.add_peer(b'\xff' * 6, channel=self.channel)

        # create objects
        self.messages = []
        self.neighbors = []

        Node.current = self

    def scan(self, rssi_limit=None, sort=False):
        self.neighbors.clear()
        for ssid, bssid, channel, rssi, security, hidden in self.sta.scan():
            if rssi_limit is not None and rssi < rssi_limit:
                continue
            if ssid.decode('utf-8').split("_")[0] == "CK":
                peer = Peer.find(ssid=ssid)
                peer.scan_rssi = rssi
                self.neighbors.append(peer)
        if sort:
            self.neighbors.sort(key=lambda n: n.rssi, reverse=True)
        else:
            shuffle(self.neighbors)
        return self.neighbors

    def send(self, message, peer=None):
        try:
            if peer is None:
                self.mesh.send(b'\xff' * 6, message, False)
            else:
                self.mesh.send(peer.bin_mac, message, False)
        except Exception as e:
            print("Can't send", f"({e})")

    def receive(self):
        self.messages.clear()
        while True:
            bin_mac, message = None, None
            try:
                bin_mac, message = self.mesh.recv(0)
            except Exception as e:
                print(e)
                break
            if bin_mac is None or message is None:
                break
            peer = Peer.find(bin_mac=bin_mac)
            peer.scan_rssi = None
            try:
                message = message.decode()
            except Exception as e:
                print(f"Received bad message ({e}) from {peer}")
            else:
                dup = False
                for msg in self.messages:
                    if msg[0] == peer:
                        dup = True
                if not dup:
                    self.messages.append((peer, message))
        return self.messages

    def add_peer(self, bin_mac):
        self.mesh.add_peer(bin_mac, channel=self.channel)

    def remove_peer(self, bin_mac):
        self.mesh.del_peer(bin_mac)


class Peer():

    seen_peers = []

    @classmethod
    def find(cls, name=None, ssid=None, bin_mac=None):
        for peer in cls.seen_peers:
            if peer.name == name or peer.ssid == ssid or peer.bin_mac == bin_mac:
                return peer
        peer = Peer(name=name, ssid=ssid, bin_mac=bin_mac)
        cls.seen_peers.append(peer)
        return peer

    def __init__(self, name=None, ssid=None, bin_mac=None):
        if not name and not ssid and not bin_mac:
            raise Exception("Peer() needs name or ssid or bin_mac")
        if name:
            self.name = name
            self.ssid = name_to_ssid(self.name)
            self.hex_mac = name_to_mac(self.name)
            self.bin_mac = hex_to_bin(self.hex_mac)
        elif ssid:
            self.ssid = ssid
            self.name = ssid_to_name(self.ssid)
            self.hex_mac = name_to_mac(self.name)
            self.bin_mac = hex_to_bin(self.hex_mac)
        elif bin_mac:
            self.bin_mac = bin_mac
            self.hex_mac = bin_to_hex(self.bin_mac)
            self.name = mac_to_name(self.hex_mac)
            self.ssid = name_to_ssid(self.name)
        self.scan_rssi = None
        print("CREATED", self)

    @property
    def rssi(self):
        if self.scan_rssi is not None:
            return self.scan_rssi
        try:
            return Node.current.mesh.peers_table[self.bin_mac][0]
        except KeyError:
            return None

    def __repr__(self):
        return f"{self.name} {self.rssi or ''}"


class O():

    pause = True

    @classmethod
    def print(cls, *args):
        if cls.pause:
            print("-----")
            cls.pause = False
        print(*args)

    @classmethod
    def reset(cls):
        cls.pause = True


def name_to_ssid(name):
    return f"CK_{name}".encode('utf-8')


def ssid_to_name(ssid):
    return "_".join(ssid.decode("utf-8").split("_")[1:])


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


def shuffle(l):
    n = len(l)
    for i in range(n - 1, 0, -1):
        j = randrange(i + 1)
        l[i], l[j] = l[j], l[i]


def find_channel(name):
    for section in topo:
        for nm in topo[section]['grid']:
            if nm == name:
                return topo[section]['channel']
    raise Exception(f"Channel not found! {name}")


def get_neighbors(name):
    for section in topo:
        for nm in topo[section]['grid']:
            if nm == name:
                x1, y1, z1 = topo[section]['grid'][name]
                distances = []
                for key in topo[section]['grid']:
                    if key == name:
                        continue
                    x2, y2, z2 = topo[section]['grid'][key]
                    distances.append((key, math.sqrt((x1 - x2)**2 + (y1 - y2)**2 + (z1 - z2)**2)))
                distances.sort(key=lambda d: d[1])
                return [distance[0] for distance in distances]
    raise Exception(f"Neighbors not found! {name}")

