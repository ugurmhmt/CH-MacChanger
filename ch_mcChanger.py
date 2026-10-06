import optparse
import os
import random as r
import re
import subprocess as sp

from colorama import Fore as f
from colorama import init

init(autoreset=True)


class MacChanger:
    os_name = os.name

    def __init__(self):
        self.parser = optparse.OptionParser(
            description="Help guide for MAC Address Changer tool"
        )
        self.parser.add_option(
            "-i",
            "--interface",
            help="Allows you to specify a network interface (default: eth0)",
            dest="interface",
        )
        self.options, _ = self.parser.parse_args()
        if self.options.interface is None:
            self.options.interface = "eth0"

    def generate_random_mac(self):
        hex_characters = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, "A", "B", "C", "D", "E", "F")
        valid_first_bytes = ["00", "02", "04", "06", "08", "0A", "0C", "0E", "42", "52"]
        first_byte = r.choice(valid_first_bytes)

        def random_char():
            return r.choice(hex_characters)

        return (
            f"{first_byte}:"
            f"{random_char()}{random_char()}:"
            f"{random_char()}{random_char()}:"
            f"{random_char()}{random_char()}:"
            f"{random_char()}{random_char()}:"
            f"{random_char()}{random_char()}"
        )

    def change_mac(self):
        if self.os_name == "posix":
            if os.geteuid() != 0:
                print(f.RED + "Root/sudo privileges are required for this action.")
                print(f.YELLOW + "Example: sudo python3 mac_changer.py -i eth0")
                return

            before_mac = self.get_interface_mac()
            if before_mac is None:
                return

            new_mac = self.generate_random_mac()

            down = sp.run(
                ["ifconfig", str(self.options.interface), "down"],
                capture_output=True,
                text=True,
            )
            if down.returncode != 0:
                print(f.RED + down.stderr)
                return

            change = sp.run(
                ["ifconfig", str(self.options.interface), "hw", "ether", new_mac],
                capture_output=True,
                text=True,
            )
            if change.returncode != 0:
                print(f.RED + change.stderr)
                sp.run(["ifconfig", str(self.options.interface), "up"])
                return

            up = sp.run(
                ["ifconfig", str(self.options.interface), "up"],
                capture_output=True,
                text=True,
            )
            if up.returncode != 0:
                print(f.RED + up.stderr)
                return

            after_mac = self.get_interface_mac()
            print(f.GREEN + f"Old MAC Address: {before_mac}")
            print(f.GREEN + f"New MAC Address: {new_mac}")

            if after_mac == new_mac:
                print(f.GREEN + "MAC address changed successfully.")
            else:
                print(f.RED + "Failed to change MAC address.")
        else:
            print(f.RED + "Unsupported operating system.")

    def get_interface_mac(self):
        if self.os_name == "posix":
            try:
                ifconfig_output = str(
                    sp.getoutput(f"ifconfig {self.options.interface}")
                )
                reg_mac = re.search(
                    r"(?i)\b[0-9a-f]{2}(?::[0-9a-f]{2}){5}\b", ifconfig_output
                )
                if reg_mac:
                    return reg_mac.group(0).upper()
                return None
            except AttributeError:
                print(f.RED + "Please specify a valid network interface.")
                return None
            except Exception as e:
                print(f.RED + str(e))
                return None


if __name__ == "__main__":
    mac_changer = MacChanger()
    mac_changer.change_mac()