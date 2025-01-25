import base64

def mac_to_name(mac):
    mac_bytes = bytes.fromhex(mac.replace(":", "").replace("-", ""))
    return base64.urlsafe_b64encode(mac_bytes).decode('utf-8')


def name_to_mac(name):
    mac_bytes = base64.urlsafe_b64decode(name)
    return ':'.join(mac_bytes.hex().upper()[i:i + 2] for i in range(0, 12, 2))


# Example usage
mac = "A8:42:E3:D8:EA:38"
compressed = mac_to_name(mac)
print("Compressed MAC Address (Fixed 8 chars):", compressed)

decompressed = name_to_mac(compressed)
print("Decompressed MAC Address:", decompressed)
