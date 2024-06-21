import subprocess
import re
import random

def get_current_mac(interface):
    try:
        ifconfig_result = subprocess.check_output(["ifconfig", interface], text=True)
        mac_address_search_result = re.search(r"ether\s+(\S+)", ifconfig_result)
        if mac_address_search_result:
            return mac_address_search_result.group(1)
        return None
    except subprocess.CalledProcessError:
        return None

def generate_random_mac():
    # Generate a valid locally-administered MAC address
    random_mac = [0x02, random.randint(0x00, 0xff), random.randint(0x00, 0xff),
                 random.randint(0x00, 0xff), random.randint(0x00, 0xff), random.randint(0x00, 0xff)]
    return ":".join([f"{byte:02x}" for byte in random_mac])

def change_mac(interface, new_mac):
    try:
        subprocess.call(["sudo", "ifconfig", interface, "down"])  # Bring interface down
        subprocess.call(["sudo", "ifconfig", interface, "hw", "ether", new_mac])
        subprocess.call(["sudo", "ifconfig", interface, "up"])    # Bring interface back up
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    active_wireless_interface = "wlp5s0"  # Your specific wireless interface name

    print(f"Active wireless interface: {active_wireless_interface}")

    current_mac = get_current_mac(active_wireless_interface)
    if not current_mac:
        print(f"Failed to retrieve MAC address of {active_wireless_interface}.")
        return

    print(f"Current MAC address of {active_wireless_interface}: {current_mac}")

    new_mac = generate_random_mac()

    if change_mac(active_wireless_interface, new_mac):
        print(f"MAC address of {active_wireless_interface} successfully changed to {new_mac}.")
    else:
        print(f"Failed to change MAC address of {active_wireless_interface}.")

if __name__ == "__main__":
    main()

