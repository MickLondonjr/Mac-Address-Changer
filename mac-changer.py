#!/usr/bin/env python

import subprocess
import optparse
import re
import random


def list_interfaces():
    # Get the output of ifconfig to list interfaces and MAC addresses
    ifconfig_result = subprocess.check_output(["ifconfig"]).decode('utf-8')
    # Find all interfaces and their corresponding MAC addresses
    interfaces = re.findall(r'(\w+): flags=\d+<.*>\n\s+ether ((?:\w{2}:){5}\w{2})', ifconfig_result)

    if interfaces:
        print("[+] Available network interfaces and their MAC addresses:")
        for interface, mac in interfaces:
            print(f"    Interface: {interface}, MAC: {mac}")
    else:
        print("[-] No network interfaces found.")


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address (leave empty for a random MAC)")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info.")
    return options


def generate_random_mac():
    return "02:%02x:%02x:%02x:%02x:%02x" % (
        random.randint(0x00, 0x7f),
        random.randint(0x00, 0xff),
        random.randint(0x00, 0xff),
        random.randint(0x00, 0xff),
        random.randint(0x00, 0xff),
        random.randint(0x00, 0xff)
    )


def change_mac(interface, new_mac):
    print("[+] Changing MAC address for " + interface + " to " + new_mac)
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


# List available network interfaces and their MAC addresses
list_interfaces()

# Get user input for interface and new MAC address
options = get_arguments()

# Generate a random MAC address if the user didn't provide one
if not options.new_mac:
    options.new_mac = generate_random_mac()
    print("[+] No MAC address provided. Generated random MAC: " + options.new_mac)

# Get and display the current MAC address
current_mac = get_current_mac(options.interface)
print("Current MAC = " + str(current_mac))

# Change the MAC address
change_mac(options.interface, options.new_mac)

# Verify and display the result
current_mac = get_current_mac(options.interface)
if current_mac == options.new_mac:
    print("[+] MAC address was successfully changed to " + current_mac)
else:
    print("[-] MAC address did not get changed.")
