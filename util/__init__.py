import sys
import os
import subprocess


def port_list():
    if not len(sys.argv) > 1:
        lines = run("mpremote connect list", True).splitlines()
        ports = [line.split("-")[-1].split(" ")[0] for line in lines
                 if "/dev/cu.usbserial" in line]
        print("[PORT]", ports)
        exit()


def run(cmd, capture=False):
    print(f"$ {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=capture)
    if capture:
        if result.returncode:
            return result.stderr.decode('utf-8')
        else:
            return result.stdout.decode('utf-8')
