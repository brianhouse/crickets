import esp32, espnow, machine
import network, ubinascii, json, random, socket, math
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
    print("MAC address is", bin_to_hex(sta.config('mac')))
    
    # start access point
    ap = network.WLAN(network.AP_IF)
    ap.config(max_clients=0) # is 0 correct? I'm just scanning
    ap.active(True)
    
    # activate mesh
    mesh = espnow.ESPNow()
    mesh.active(True)
    

def send(message):
    try:
        for peer in peers:
            try:
                mesh.send(peer, message)
            except Exception as exc:
                print("Can't send to", bin_to_hex(peer))
    except NameError:
        raise Exception("Wifi not started")


def receive():
    try:
        sender, msg = mesh.recv(0)
        if msg and sender in peers:
            return bin_to_hex(sender), msg.decode()
        else:
            return None, None
    except NameError:
        raise Exception("Wifi not started")


def add_peer(hex_mac):
    try:
        bin_mac = hex_to_bin(hex_mac)
        mesh.add_peer(bin_mac)
        peers.append(bin_mac)
    except NameError:
        raise Exception("Wifi not started")        


def bin_to_hex(bin_mac):
    return ubinascii.hexlify(bin_mac, ':').decode().upper()


def hex_to_bin(hex_mac):
    return ubinascii.unhexlify(hex_mac.replace(':', '').lower())


def map(value, in_min, in_max, out_min, out_max):
    value = (value - in_min) / float(in_max - in_min)
    return (value * (out_max - out_min)) + out_min








