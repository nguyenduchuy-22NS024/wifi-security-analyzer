import subprocess

from services.detect_suspicious_aps import DetectSuspiciousAps


class WifiService:
    def __init__(self):
        self.detect_suspicious_aps = DetectSuspiciousAps([])

    # Scan wifi networks on the given interface
    def scan_networks(self, interface):
        result = subprocess.run(
            [
                "nmcli",
                "-t",
                "-f",
                "SSID,SSID-HEX,BSSID,MODE,CHAN,FREQ,RATE,BANDWIDTH,SIGNAL,BARS,SECURITY,WPA-FLAGS,RSN-FLAGS,ACTIVE,IN-USE",
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
        keys = [
            "ssid",
            "ssid_hex",
            "bssid",
            "mode",
            "chan",
            "freq",
            "rate",
            "bandwidth",
            "signal",
            "bars",
            "security",
            "wpa_flags",
            "rsn_flags",
            "active",
            "in_use",
        ]

        for line in result.stdout.strip().split("\n"):

            # Fix escape "\:" and split by ":"
            # print(line)
            line = line.replace("\\:", "[COLON]")
            parts = line.split(":")
            parts = [p.replace("[COLON]", ":") for p in parts]
            # print(parts)

            if len(parts) < len(keys):
                continue

            ap = dict(zip(keys, parts))
            ap["security_level"] = self.evaluate_security(
                ap["security"], ap["wpa_flags"], ap["rsn_flags"]
            )
            ap["signal_level"] = self.signal_level(ap["signal"])

            networks.append(ap)
        return networks

    

    # Convert signal strength to level
    def signal_level(self, signal):
        signal = int(signal)

        if signal >= 80:
            return "Excellent"
        elif signal >= 60:
            return "Good"
        elif signal >= 40:
            return "Fair"
        elif signal >= 20:
            return "Weak"
        return "Very Weak"

    def get_interfaces(self):
        result = subprocess.run(["iw", "dev"], capture_output=True, text=True)

        # print(result)
        interfaces = []
        for line in result.stdout.splitlines():
            if "Interface" in line:
                ifname = line.split()[1]
                interfaces.append(ifname)

        return interfaces

    # Analyze scan results for dashboard stats
    def analyze_dashboard(self, networks):
        total_aps = len(networks)

        strong = 0
        medium = 0
        weak = 0
        open_net = 0

        for ap in networks:
            sec = ap["security_level"]

            if "Low Risk" in sec:
                strong += 1

            elif "Medium Risk" in sec:
                medium += 1

            elif "High Risk" in sec or "Critical" in sec:
                weak += 1

            elif "Open" in sec or "Unknown" in sec:
                open_net += 1

        self.detect_suspicious_aps.networks = networks
        suspicious_list = self.detect_suspicious_aps.detect()
        weak_total = medium + weak + open_net

        return {
            "total": total_aps,
            "strong": strong,
            "medium": medium,
            "weak": weak,
            "open": open_net,
            "weak_total": weak_total,
            "suspicious": suspicious_list,
        }


# print(WifiService().scan_networks("wlp1s0"))
