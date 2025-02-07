import sys
import os
import subprocess
import pickle
import json


def port_list():
    if not len(sys.argv) > 1:
        lines = run("venv/bin/mpremote connect list", True).splitlines()
        ports = [line.split("-")[-1].split(" ")[0] for line in lines]
        ports = [port for port in ports if len(port) > 1 and "/dev" in port]
        print("PORTS:", ports)
        exit()


def run(cmd, capture=False):
    print(f"$ {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=capture)
    if capture:
        if result.returncode:
            return result.stderr.decode('utf-8')
        else:
            return result.stdout.decode('utf-8')


def save(filename, data):
    with open(filename, 'wb') as f:
        pickle.dump(data, f)


def load(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)
