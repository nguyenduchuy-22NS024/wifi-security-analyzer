from collections import defaultdict

def detect_suspicious_networks(networks):
    ssid_groups = defaultdict(list)
    for ap in networks:
        ssid = ap.get("ssid") or ap.get("details", {}).get("SSID")
        if ssid:
            ssid_groups[ssid].append(ap)

    suspicious_results = []

    for ssid, aps in ssid_groups.items():
        if len(aps) <= 1:
            continue

        reasons = []
        risk_score = 0

        # --- Rule 1: Security/Cipher Mismatch (Trọng số rất cao) ---
        # Kiểm tra xem có cái dùng WPA2, cái dùng Open không
        securities = set()
        for ap in aps:
            dtl = ap.get("details", {})
            sec_type = "Open"
            if "RSN" in dtl or "WPA" in dtl:
                sec_type = "WPA2/WPA3"
            securities.add(sec_type)

        if len(securities) > 1:
            reasons.append(f"Security mismatch: {securities}")
            risk_score += 50

        # --- Rule 2: TSF Anomaly (Uptime chênh lệch quá lớn) ---
        tsf_values = []
        for ap in aps:
            tsf = ap.get("details", {}).get("TSF")
            if tsf:
                # TSF format: "4450268683052 usec (51d, 12:11:08)"
                # Lấy phần số usec đầu tiên
                try:
                    val = int(tsf.split()[0])
                    tsf_values.append(val)
                except:
                    pass

        if len(tsf_values) > 1:
            uptime_diff_days = (max(tsf_values) - min(tsf_values)) / (10**6 * 3600 * 24)
            if uptime_diff_days > 7:  # Chênh lệch hơn 7 ngày uptime
                reasons.append(
                    f"Uptime mismatch: {uptime_diff_days:.1f} days difference"
                )
                risk_score += 20

        # --- Rule 3: Capability Mismatch (HT/VHT/HE) ---
        # Kiểm tra chuẩn WiFi (WiFi 4/5/6)
        standards = set()
        for ap in aps:
            dtl = ap.get("details", {})
            if "HE capabilities" in dtl:
                standards.add("WiFi 6 (HE)")
            elif "VHT capabilities" in dtl:
                standards.add("WiFi 5 (VHT)")
            elif "HT capabilities" in dtl:
                standards.add("WiFi 4 (HT)")

        if len(standards) > 1:
            reasons.append(f"Standard mismatch: {list(standards)}")
            risk_score += 30

        # --- Rule 4: Vendor (OUI) Mismatch ---
        ouis = set(ap["bssid"].upper()[:8] for ap in aps)
        if len(ouis) > 1:
            reasons.append(f"Different vendors (OUI): {list(ouis)}")
            risk_score += 25

        # --- Rule 5: Country Code Mismatch ---
        countries = set()
        for ap in aps:
            c = ap.get("details", {}).get("Country", {}).get("Code")
            if c:
                countries.add(c)

        if len(countries) > 1:
            reasons.append(f"Country code mismatch: {countries}")
            risk_score += 15

        # --- Rule 6: Signal & Channel Anomaly ---
        for ap in aps:
            freq = float(ap.get("details", {}).get("freq", 0))
            # Nếu tên có "5G" mà freq < 3000MHz (2.4GHz)
            if "5G" in ssid.upper() and freq < 3000:
                reasons.append(
                    f"5G SSID on 2.4GHz freq ({freq}MHz) at BSSID {ap['bssid']}"
                )
                risk_score += 40

        # Phân loại rủi ro dựa trên tổng điểm
        if risk_score > 0:
            risk_level = "Low"
            if risk_score >= 60:
                risk_level = "Critical"
            elif risk_score >= 40:
                risk_level = "High"
            elif risk_score >= 20:
                risk_level = "Medium"

            suspicious_results.append(
                {
                    "ssid": ssid,
                    "risk_level": risk_level,
                    "score": risk_score,
                    "reasons": reasons,
                    "ap_details": [
                        {
                            "bssid": a["bssid"],
                            "freq": a.get("details", {}).get("freq"),
                            "signal": a.get("details", {}).get("signal"),
                        }
                        for a in aps
                    ],
                }
            )

    return suspicious_results
