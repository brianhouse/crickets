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
        #print(self.sta.config("txpower"))
        self.mac = bin_to_hex(self.sta.config('mac'))
        self.name = mac_to_name(self.mac)

        # start access point
        self.ap = network.WLAN(network.AP_IF)
        self.ap.active(True)
        self.ap.config(ssid=name_to_ssid(self.name), password="pulsecoupled", authmode=network.AUTH_WPA2_PSK)

        # activate mesh
        self.mesh = espnow.ESPNow()
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

    def send(self, message):
        for peer in self.peers:
            try:
                self.mesh.send(hex_to_bin(name_to_mac(peer)), message)
            except Exception:
                print("Can't send to", peer)

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


def map(value, in_min, in_max, out_min, out_max):
    value = (value - in_min) / float(in_max - in_min)
    return (value * (out_max - out_min)) + out_min


def reverse(s):
    return "".join(reversed([c for c in s]))


mesh = Mesh()
