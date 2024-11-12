#!venv/bin/python

from util import *


port_list()

port = f"/dev/cu.usbserial-{sys.argv[1]}"

if len(sys.argv) < 3:
    print("[COMMAND]")
    exit()
command = sys.argv[2]

run(f"mpremote connect {port} cp manager/util.py :util.py")
run(f"mpremote connect {port} soft-reset sleep 0.5 bootloader")
run(f"mpremote connect {port} run manager/{command}.py")
