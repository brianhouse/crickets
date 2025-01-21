# firmware: https://micropython.org/download/esp32/
# choose the usbserial, not the SLAB

if [[ $# -eq 0 ]]
  then
    echo "[PORT]"
    ls -la /dev/tty.*
    exit 1
fi
PORT=$1
echo $PORT
read -p "Erase $PORT [y/N]? " -n 1 -r
if [[ $REPLY =~ ^[Yy]$ ]]
then
    echo "Flashing..."
    esptool.py --chip esp32 --port $PORT --baud 115200 erase_flash
    esptool.py --chip esp32 --port $PORT --baud 115200 write_flash -z 0x1000 ESP32_GENERIC-20241129-v1.24.1.bin
    echo "--> done"
else
    echo "Exiting..."
fi
