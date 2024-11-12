#!venv/bin/python

from util import *


port_list()

port = f"/dev/cu.usbserial-{sys.argv[1]}"

# run(f"mpremote connect {port} fs ls")
for filename in os.listdir("cricket/"):
    if filename.split(".")[-1] != "py":
        continue
    run(f"mpremote connect {port} cp cricket/{filename} :{filename}")
    print()

run(f"mpremote connect {port} soft-reset sleep 0.5 bootloader")
run(f"mpremote connect {port} exec --no-follow 'import main.py'")
run(f"mpremote connect {port}")
