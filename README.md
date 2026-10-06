# 🛡️ CH-MacChanger

A lightweight, automated Python tool designed to randomize and spoof network interface MAC addresses on Linux systems safely and efficiently.

It generates valid locally-administered MAC prefixes, handles root privilege checks, and validates address modifications via output regex parsing.

---

## 📌 Repository Description & Topics

**Short Description:**  
> A Python CLI tool for Linux to spoof, randomize, and verify Network Interface Card (NIC) MAC addresses automatically.

**Topics:**  
`python3` `mac-changer` `kali-linux` `mac-spoofing` `cybersecurity` `networking` `ethical-hacking` `penetration-testing`

---

## ✨ Features

- **Automated Random Generation:** Generates valid unicast/locally administered MAC addresses to prevent network rejection.
- **Verification Engine:** Confirms the actual interface MAC change post-execution using regex parsing.
- **Safety Checks:** Automatically verifies root (`sudo`) permissions before executing system network modifications.
- **Colorized CLI Output:** Styled status and error messages powered by `colorama`.
- **Custom Interface Support:** Specify any target network interface (`eth0`, `wlan0`, `enp3s0`, etc.) using command-line flags.

---

## 🚀 Installation & Requirements

### Prerequisites

Ensure Python 3 and system networking utilities (`net-tools`) are installed on your Linux machine:

```bash
sudo apt update && sudo apt install python3 net-tools -y
```

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/CH-MacChanger.git
   cd CH-MacChanger
   ```

2. **Install Python dependencies:**
   ```bash
   pip install colorama
   ```

---

## 💻 Usage

> ⚠️ **Note:** Root privileges (`sudo`) are required to modify system network interface properties.

### Default Usage (Interface: `eth0`)
```bash
sudo python3 ch_mcChanger.py
```

**Example Output:**
```text
Old MAC Address: 38:F3:AB:68:45:18
New MAC Address: 0C:3F:3B:33:F1:3E
MAC address changed successfully.
```

### Custom Interface Selection
To change the MAC address of a specific interface (e.g., wireless card `wlan0`):

```bash
sudo python3 ch_mcChanger.py -i wlan0
```

### Help Menu
```bash
python3 ch_mcChanger.py --help
```

---

## ⚙️ How It Works

1. **Privilege Verification:** Checks `os.geteuid()` to ensure execution with elevated privileges.
2. **Current MAC Extraction:** Reads network interface details via `ifconfig` and parses the active MAC address using Regex (`re.search`).
3. **Valid OUI Generation:** Constructs a random 6-byte hexadecimal MAC string using valid unicast prefixes (`00`, `02`, `0A`, `42`, etc.).
4. **Safe Interface State Toggle:** Toggles the target interface down, updates the hardware address (`hw ether`), and restores the interface back up.
5. **State Validation:** Re-queries the interface post-change to confirm whether the OS accepted the new hardware address.

---

## ⚠️ Disclaimer

This tool is created strictly for **educational purposes** and **authorized security testing/auditing**. The developer assumes no liability for misuse or unauthorized activities on computer networks.