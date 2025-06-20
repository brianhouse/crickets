#!venv/bin/python

from util import *


port_list()

port = sys.argv[1]

# run(f"mpremote connect {port} fs ls")
for filename in os.listdir("cricket/"):
    if filename.split(".")[-1] not in ["py", "json"]:
        continue
    run(f"venv/bin/mpremote connect {port} cp cricket/{filename} :{filename}")
    print()

run(f"venv/bin/mpremote connect {port} soft-reset sleep 0.5 bootloader")
run(f"venv/bin/mpremote connect {port} exec --no-follow 'import main.py'")
run(f"venv/bin/mpremote connect {port}")
