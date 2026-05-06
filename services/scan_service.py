import subprocess


class WifiScanService:

    def __init__(self):
        self.wifi_networks = {}

    # Quét toàn bộ wifi xung quanh
    def scan_wifi_networks(self, interface: str):
        cmd = subprocess.run(
            ["iw", "dev", interface, "scan"], capture_output=True, text=True
        )
        
        raw_data = cmd.stdout
        for bss


    def parse_raw_scan_wifi_networks(self, raw_data):
        
        pass
    
    # Lấy interface wifi
    def get_network_interfaces(self):
        interfaces = []
        cmd = subprocess.run(["iw", "dev"], capture_output=True, text=True)
        for line in cmd.stdout.splitlines():
            if "Interface" in line:
                ifname = line.split()[1]
                interfaces.append(ifname)

        return interfaces

