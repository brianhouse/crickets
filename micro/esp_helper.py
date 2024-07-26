import network
import ubinascii
import math
import espnow
from machine import ADC, Pin, PWM
from time import sleep, sleep_ms, ticks_ms, ticks_us
from random import random, randint, choice

# https://learn.adafruit.com/huzzah32-esp32-breakout-board/pinouts


STA = Pin(13, Pin.OUT)
LED = Pin(21, Pin.OUT)
PIR = Pin(33, Pin.IN)
SND = PWM(Pin(27, Pin.OUT))
SND.duty(0)


peers = []


def start_wifi():
    global mesh, sta, ap

    # start wifi receiver
    sta = network.WLAN(network.STA_IF)
    sta.active(True)

    # start access point
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(max_clients=0)

    # activate mesh
    mesh = espnow.ESPNow()
    mesh.active(True)

    print("MAC address is", bin_to_hex(sta.config('mac')))


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


def send(message):
    try:
        for peer in peers:
            try:
                mesh.send(hex_to_bin(peer), message)
            except Exception:
                print("Can't send to", peer)
    except NameError:
        raise Exception("Wifi not started")


def receive():
    try:
        sender, msg = mesh.recv(0)
        if msg and sender:
            sender = bin_to_hex(sender)
            return sender, msg.decode()
        else:
            return None, None
    except NameError:
        raise Exception("Wifi not started")


def add_peer(mac):
    try:
        mesh.add_peer(hex_to_bin(mac))
        peers.append(mac)
    except NameError:
        raise Exception("Wifi not started")


def clear_peers():
    try:
        for peer in peers:
            mesh.del_peer(peer)
        peers.clear()
    except NameError:
        raise Exception("Wifi not started")


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



