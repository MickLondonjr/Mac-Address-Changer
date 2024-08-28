# MAC Address Changer

This script allows you to change the MAC address of a network interface on a Linux system. You can specify a new MAC address manually or allow the script to generate a random one for you.

## Features

- Lists all available network interfaces with their current MAC addresses.
- Allows the user to specify a new MAC address or generates a random one if none is provided.
- Changes the MAC address of the specified interface.
- Validates that the MAC address was successfully changed.

## Requirements

- Python 3.x
- `ifconfig` command (available on most Linux distributions)

## Usage

1. **Clone the Repository**

   ```bash
   git clone https://github.com/MickLondonjr/Mac-Address-Changer.git
   cd Mac-Address-Changer
   ```

2. **Run the Script**

   You can run the script with or without arguments:

   - **To list interfaces and change the MAC address of a specific interface with a manually specified MAC:**

     ```bash
     sudo ./mac-changer.py -i eth0 -m 00:11:22:33:44:55
     ```

   - **To list interfaces and change the MAC address of a specific interface with a randomly generated MAC:**

     ```bash
     sudo ./mac-changer.py -i eth0
     ```

   - **To simply list the available network interfaces and their MAC addresses:**

     Run the script without any arguments, and it will display the available interfaces.

## Example Output

```bash
$ sudo ./mac-changer.py

[+] Available network interfaces and their MAC addresses:
    Interface: eth0, MAC: 02:22:cd:6c:e6:72
    Interface: wlan0, MAC: 00:11:22:33:44:55

Usage: mac-changer.py [options]

mac-changer.py: error: [-] Please specify an interface, use --help for more info.
```

```bash
$ sudo ./mac-changer.py -i eth0
[+] No MAC address provided. Generated random MAC: 02:4b:7c:2d:3e:8f
Current MAC = 02:22:cd:6c:e6:72
[+] Changing MAC address for eth0 to 02:4b:7c:2d:3e:8f
[+] MAC address was successfully changed to 02:4b:7c:2d:3e:8f
```

## Notes

- Ensure you have the necessary permissions to change the MAC address of network interfaces (usually requires `sudo`).
- The script was tested on a Linux environment. It may not work as expected on non-Linux systems.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```

This `README.md` provides an overview of the project, instructions on how to use it, and an example of the output. It should be clear and helpful for users who want to use your MAC address changer script.
