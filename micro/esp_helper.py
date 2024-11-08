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

# https://learn.adafruit.com/huzzah32-esp32-breakout-board/pinouts
STA = Pin(13, Pin.OUT)
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

        # start access point
        self.ap = network.WLAN(network.AP_IF)
        self.ap.active(True)
        self.ap.config(password='pulsecoupled', authmode=network.AUTH_WPA2_PSK)

        # activate mesh
        self.mesh = espnow.ESPNow()
        self.mesh.active(True)

        self.mac = bin_to_hex(self.sta.config('mac'))
        self.ip = self.ap.ifconfig()[0]
        self.ssid = self.ap.config('essid')
        self.name = self.ssid.split("_")[-1]
        print(f"## {self.name} ##")

    def scan(self):
        self.neighbors = []
        for ssid, bssid, channel, rssi, security, hidden in self.sta.scan():
            if ssid.decode('utf-8').split("_")[0] == "ESP":
                self.neighbors.append({'name': ssid_to_name(ssid),
                                       'rssi': rssi}
                                      )
        self.neighbors.sort(key=lambda n: n['rssi'], reverse=True)
        return self.neighbors

    def send(self, message):
        for peer in self.peers:
            try:
                self.mesh.send(hex_to_bin(name_to_mac(peer)), message)
            except Exception:
                print("Can't send to", peer)

    def receive(self):
        sender, msg = self.mesh.recv(0)
        if msg and sender:
            sender = mac_to_name(bin_to_hex(sender))
            return sender, msg.decode()
        else:
            return None, None

    def connect(self, ssid):
        if self.sta.isconnected():
            self.sta.disconnect()
        print(f"Connecting to {ssid.decode('utf-8')}...")
        try:
            self.sta.connect(ssid, "pulsecoupled")
        except Exception as e:
            print(e)
        while not self.sta.isconnected():
            status = self.sta.status()
            if status in STATUS_CODES:
                print(STATUS_CODES[status])
            else:
                print(".")
            sleep(1)
        print("--> connected")

    def add_peer(self, name):
        self.mesh.add_peer(hex_to_bin(name_to_mac(name)))
        self.peers.append(name)

    def clear_peers(self):
        for peer in self.peers:
            try:
                self.mesh.del_peer(hex_to_bin(name_to_mac(peer)))
            except ValueError as e:
                print(e)
        self.peers.clear()


def name_to_ssid(name):
    return f"ESP_{name}".encode('utf-8')


def ssid_to_name(ssid):
    return ssid.decode("utf-8").split("_")[-1]


def name_to_mac(name):
    return f"7C:9E:BD:{name[:2]}:{name[2:4]}:{name[4:]}"


def mac_to_name(mac):
    return "".join(mac.split(":")[3:])


def ap_to_peer(hex_mac):
    # subtract 1 from the last octet to find the peer address
    return hex_mac[:-2] + hex(int(hex_mac.split(':')[-1], 16) - 1)[-2:].upper()


def bin_to_hex(bin_mac):
    return ubinascii.hexlify(bin_mac, ':').decode().upper()


def hex_to_bin(hex_mac):
    return ubinascii.unhexlify(hex_mac.replace(':', '').lower())


def map(value, in_min, in_max, out_min, out_max):
    value = (value - in_min) / float(in_max - in_min)
    return (value * (out_max - out_min)) + out_min


# connection status codes
STATUS_CODES = {200: 'BEACON_TIMEOUT',
                201: 'NO_AP_FOUND',
                202: 'WRONG_PASSWORD',
                203: 'ASSOC_FAIL',
                204: 'HANDSHAKE_TIMEOUT',
                1000: 'IDLE',
                1001: 'CONNECTING',
                1010: 'GOT_IP'
                }

mesh = Mesh()



