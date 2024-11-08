#!venv/bin/python

import os, sys, subprocess

if not len(sys.argv) > 1:
    print("[PORT]")
    exit()

port = f"/dev/cu.usbserial-{sys.argv[1]}"
subprocess.run(f"mpremote connect {port} cp micro/esp_helper.py :esp_helper.py", shell=True)
subprocess.run(f"mpremote connect {port} soft-reset sleep 0.5 bootloader", shell=True)
subprocess.run(f"mpremote connect {port} run manager.py", shell=True)