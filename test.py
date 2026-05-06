import subprocess


def scan_wifi(interface):
    result = subprocess.run(
        [
            "nmcli",
            "-t",
            "-f",
            "ALL",
            "device",
            "wifi",
            "list",
            "ifname",
            interface,
        ],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print("Error:", result.stderr)
        return []

    networks = []

    for line in result.stdout.strip().split("\n"):
        ap = parse_nmcli_line(line)
        if not ap:
            continue

        ap["security_level"] = analyze_security(ap["security"])
        ap["signal_level"] = signal_level(ap["signal"])

        networks.append(ap)

    print(networks)


def parse_nmcli_line(line):
    # Fix escape "\:"
    line = line.replace("\\:", "[COLON]")
    parts = line.split(":")
    parts = [p.replace("[COLON]", ":") for p in parts]

    try:
        return {
            "in_use": parts[0] == "*",
            "ssid": parts[1],
            "ssid_hex": parts[2],
            "bssid": parts[3],
            "mode": parts[4],
            "channel": int(parts[5]) if parts[5].isdigit() else None,
            "frequency": parts[6],
            "rate": parts[7],
            "bandwidth": parts[8],
            "signal": int(parts[9]) if parts[9].isdigit() else 0,
            "bars": parts[10],
            "security": parts[11],
            "device": parts[14],
            "active": parts[15] == "yes",
        }
    except IndexError:
        return None


def analyze_security(sec):
    if "WEP" in sec:
        return "Very Weak"
    elif "WPA1" in sec:
        return "Weak"
    elif "WPA2" in sec and "WPA1" not in sec:
        return "Good"
    elif "WPA3" in sec:
        return "Strong"
    elif sec.strip() == "":
        return "Open"
    return "Unknown"


def signal_level(signal):
    if signal > 80:
        return "Excellent"
    elif signal > 60:
        return "Good"
    elif signal > 40:
        return "Medium"
    return "Weak"


scan_wifi("wlp1s0")
