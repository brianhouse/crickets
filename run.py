#!venv/bin/python

from util import *

port_list()

port = sys.argv[1]

if len(sys.argv) < 3:
    print("[PORT] [COMMAND]")
    exit()
command = sys.argv[2]
run(f"venv/bin/mpremote connect {port} cp crickets.json :crickets.json")
if command == "post":
    if len(sys.argv) < 4:
        print("post [filename]")
        exit()
    filename = sys.argv[3]
    if filename in os.listdir("manager"):
        print("--> conflicting filename!")
        exit()
    with open("cricket/update.txt", 'w') as f:
        f.write(filename + "\n")
    run(f"venv/bin/mpremote connect {port} cp cricket/{filename} :{filename}")
    run(f"venv/bin/mpremote connect {port} cp cricket/update.txt :update.txt")

run(f"venv/bin/mpremote connect {port} cp manager/net.py :net.py")
run(f"venv/bin/mpremote connect {port} soft-reset sleep 0.5 bootloader")
run(f"venv/bin/mpremote connect {port} run manager/{command}.py")
