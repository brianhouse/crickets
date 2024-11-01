#!venv/bin/python

import os, sys, subprocess

if not len(sys.argv) > 1:
    print("[PORT]")
    exit()

port = f"/dev/cu.usbserial-{sys.argv[1]}"
subprocess.run(f"mpremote connect {port}", shell=True)