#!/usr/bin/env python3

import subprocess
import optparse
import re
import random


def list_interfaces():
    # Get the output of ifconfig to list interfaces and MAC addresses
    try:
        ifconfig_result = subprocess.check_output(["ifconfig"]).decode('utf-8')
        # Debug print to see the raw ifconfig result
        print("[DEBUG] ifconfig output:\n", ifconfig_result)

        # Find all interfaces and their corresponding MAC addresses
        interfaces = re.findall(r'(\w+):\s+flags=.*?ether ((?:\w{2}:){5}\w{2})', ifconfig_result)

        if interfaces:
            print("[+] Available network interfaces and their MAC addresses:")
            for interface, mac in interfaces:
                print(f"    Interface: {interface}, MAC: {mac}")
        else:
            print("[-] No network interfaces found.")
    except subprocess.CalledProcessError as e:
        print(f"[-] Error occurred while running ifconfig: {e}")


def get_arguments():
    parser = optparse.OptionParser()
    list_interfaces()  # List interfaces before asking for input
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC Address (leave empty to generate a random MAC)")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info.")
    return options


def generate_random_mac():
    return "02:%02x:%02x:%02x:%02x:%02x:%02x" % (
        random.randint(0x00, 0x7f),
        random.randint(0x00, 0xff),
        random.randint(0x00, 0xff),
        random.randint(0x00, 0xff),
        random.randint(0x00, 0xff),
        random.randint(0x00, 0xff)
    )


def change_mac(interface, new_mac):
    print(f"[+] Changing MAC address for {interface} to {new_mac}")
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])


def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result))
    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("[-] Could not read MAC address.")


options = get_arguments()

# Generate a random MAC address if none is provided
if not options.new_mac:
    options.new_mac = generate_random_mac()
    print(f"[+] No MAC address provided. Generated random MAC: {options.new_mac}")

current_mac = get_current_mac(options.interface)
print(f"Current MAC = {current_mac}")

change_mac(options.interface, options.new_mac)

current_mac = get_current_mac(options.interface)
if current_mac == options.new_mac:
    print(f"[+] MAC address was successfully changed to {current_mac}")
else:
    print("[-] MAC address did not get changed.")
