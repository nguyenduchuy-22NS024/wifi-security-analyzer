class EvaluateSecurity():
    def __init__(self):
        pass

def evaluate_security(self, sec, wpa_flags="", rsn_flags=""):
        sec = sec.upper()
        flags = (wpa_flags + " " + rsn_flags).upper()

        # 1. Mạng Open (nmcli trả về "--")
        if "--" in sec or sec.strip() == "":
            return "Critical (Open Network - No Encryption)"

        # 2. WEP (Rất yếu)
        if "WEP" in sec:
            return "Critical (WEP)"

        # 3. WPA 1
        # nmcli có thể ghi là "WPA1" hoặc chỉ "WPA"
        is_wpa1 = "WPA1" in sec or (
            "WPA" in sec and "WPA2" not in sec and "WPA3" not in sec
        )

        if is_wpa1:
            if "WPA2" in sec:
                if "TKIP" in flags:
                    return "Critical (Mixed WPA1/WPA2 + TKIP)"
                return "High Risk (Mixed WPA1/WPA2)"
            return "High Risk (WPA1)"

        # 4. WPA2
        if "WPA2" in sec:
            # Kiểm tra TKIP trong WPA2
            if "TKIP" in flags:
                return "High Risk (WPA2 with TKIP)"

            # Nếu có cả WPA3 hoặc SAE thì là Transition Mode
            if "WPA3" in sec or "SAE" in sec:
                return "Medium Risk (WPA3 Transition Mode)"

            # Kiểm tra Enterprise
            if "802.1X" in sec:
                return "Low Risk (WPA2 Enterprise)"

            return "Medium Risk (WPA2-PSK AES)"

        # 5. WPA3
        if "WPA3" in sec or "SAE" in sec:
            return "Low Risk (WPA3)"

        return "Unknown Security"