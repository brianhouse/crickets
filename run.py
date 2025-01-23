#!venv/bin/python

from util import *


port_list()

port = sys.argv[1]

if len(sys.argv) < 3:
    print("[PORT] [COMMAND]")
    exit()
command = sys.argv[2]
if command == "post":
    if len(sys.argv) < 4:
        print("post [filename]")
        exit()
    filename = sys.argv[3]
    if filename in ['hello', 'net', 'peers', 'post']:
        print("--> conflicting filename!")
        exit()
    run(f"venv/bin/mpremote connect {port} cp cricket/{filename} :{filename}")

run(f"venv/bin/mpremote connect {port} cp manager/net.py :net.py")
run(f"venv/bin/mpremote connect {port} soft-reset sleep 0.5 bootloader")
run(f"venv/bin/mpremote connect {port} run manager/{command}.py")
