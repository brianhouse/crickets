#!venv/bin/python

import os, sys, subprocess, time, mpremote


def run(cmd):
    print(f"$ {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True)
    if result.returncode:
        return result.stderr.decode('utf-8')
    else:
        return result.stdout.decode('utf-8')


if not len(sys.argv) > 1:
    lines = run("mpremote connect list").splitlines()
    ports = [line.split("-")[-1].split(" ")[0] for line in lines
             if "/dev/cu.usbserial" in line]
    print("[PORT]", ports)
    exit()

port = f"/dev/cu.usbserial-{sys.argv[1]}"

print(run(f"mpremote connect {port} fs ls"))

for filename in os.listdir("micro/"):
    if filename.split(".")[-1] != "py":
        continue
    print(run(f"mpremote connect {port} cp micro/{filename} :{filename}"))

print(run(f"mpremote connect {port} soft-reset sleep 0.5 bootloader"))
print(run(f"mpremote connect {port} exec --no-follow 'import main.py'"))
