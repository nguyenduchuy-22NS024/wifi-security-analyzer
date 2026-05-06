from collections import defaultdict


class DetectSuspiciousAps:

    def __init__(self, networks):
        self.networks = networks

    def detect(self):
        ssid_groups = defaultdict(list)

        # Group by SSID
        for ap in self.networks:
            if ap["ssid"]:
                ssid_groups[ap["ssid"]].append(ap)

        suspicious_results = []

        for ssid, aps in ssid_groups.items():
            if len(aps) <= 1:
                continue

            reasons = []

            # --- Rule 1: Multiple BSSID
            bssids = set(ap["bssid"] for ap in aps)
            if len(bssids) > 1:
                reasons.append("Multiple BSSID")

            # --- Rule 2: Security mismatch
            securities = set(ap["security"] for ap in aps)
            if len(securities) > 1:
                reasons.append("Security mismatch")

            # --- Rule 3: Channel/Freq anomaly
            chans = [int(ap["chan"]) for ap in aps if ap["chan"].isdigit()]
            if "5G" in ssid and any(c <= 14 for c in chans):
                reasons.append("5G SSID on 2.4GHz channel")

            # --- Rule 4: Vendor mismatch (OUI)
            def get_oui(bssid):
                return bssid[:8]

            ouis = set(get_oui(ap["bssid"]) for ap in aps)
            if len(ouis) > 1:
                reasons.append("Different vendors (OUI mismatch)")

            # --- Rule 5: Signal anomaly
            signals = [int(ap["signal"]) for ap in aps]
            if max(signals) - min(signals) > 30:
                reasons.append("Abnormal signal difference")

            # Classify risk level
            if len(reasons) >= 2:
                suspicious_results.append(
                    {"ssid": ssid, "risk": "High", "reasons": reasons, "aps": aps}
                )
            elif len(reasons) == 1:
                suspicious_results.append(
                    {"ssid": ssid, "risk": "Medium", "reasons": reasons, "aps": aps}
                )

        return suspicious_results
