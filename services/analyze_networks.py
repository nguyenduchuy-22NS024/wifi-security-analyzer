from services.scan_networks import detect_suspicious_networks, evaluate_security
from collections import defaultdict
import re


def analyze_network(target_bssid, networks):
    target_bssid = target_bssid.lower()
    net = next(
        (n for n in networks if n.get("bssid", "").lower() == target_bssid), None
    )

    if not net:
        return None

    details = net.get("details", {})
    ssid = details.get("SSID", "N/A")
    score_history = []  # Tracks the scoring process

    # --- 1. SUSPICIOUS NETWORK DETECTION ---
    suspicious_list = detect_suspicious_networks(networks)
    suspicious_data = next(
        (item for item in suspicious_list if item["ssid"] == ssid), None
    )

    # --- 2. BASIC INFORMATION COLLECTION ---
    freq = float(details.get("freq", 0))
    band = "5GHz" if freq > 4000 else "2.4GHz"
    channel = details.get("DS Parameter set", "N/A")
    interface = net.get("interface", "N/A")
    try:
        signal = int(float(details.get("signal", "-100").split()[0]))
    except:
        signal = -100

    security_status = evaluate_security(details)
    quality = evaluate_network_quality(details)

    # --- 3. BASE SCORE CALCULATION ---
    base_score, base_breakdown = calculate_base_score(
        details, signal, band, security_status
    )
    score_history.extend(base_breakdown)

    # --- 4. APPLY PENALTY MULTIPLIER ---
    multiplier = 1.0
    penalty_reason = ""

    if suspicious_data:
        risk_lvl = suspicious_data["risk_level"]
        if risk_lvl == "CRITICAL":
            multiplier = 0.4
            penalty_reason = (
                "CRITICAL spoofing/Rogue AP attempt detected (60% score reduction)"
            )
        elif risk_lvl == "HIGH":
            multiplier = 0.6
            penalty_reason = (
                "HIGH-risk abnormal activity detected (40% score reduction)"
            )
        else:
            multiplier = 0.8
            penalty_reason = "System security warning (20% score reduction)"
    else:
        # Penalty for configuration flaws
        if "Critical" in security_status:
            multiplier = 0.5
            penalty_reason = (
                "Critical security flaw - legacy encryption protocol (50% reduction)"
            )
        elif "High Risk" in security_status:
            multiplier = 0.7
            penalty_reason = "High-risk security configuration (30% reduction)"
        elif "Medium Risk" in security_status:
            multiplier = 0.9
            penalty_reason = "Sub-optimal security configuration (10% reduction)"

    if multiplier < 1.0:
        score_history.append(f"- Penalty Multiplier: {multiplier} ({penalty_reason})")

    final_score = int(base_score * multiplier)
    final_score = max(10, min(100, final_score))

    # Integrate alerts into Cons
    pros = quality.get("pros", [])
    cons = quality.get("cons", [])
    if suspicious_data:
        cons.insert(
            0, f"⚠️ SECURITY ALERT: Flagged as {suspicious_data['risk_level']} RISK!"
        )
        for r in suspicious_data["reasons"]:
            cons.append(f"❗ {r}")

    return {
        "SSID": ssid,
        "BSSID": target_bssid.upper(),
        "Security": security_status,
        "Freq": f"{freq} MHz",
        "Channel": f"{channel} ({band})",
        "Interface": interface,
        "Signal": f"{signal} dBm",
        "Score": final_score,
        "ScoreBreakdown": score_history,
        "Pros": pros,
        "Cons": cons,
        "Details": details,
    }


def calculate_base_score(details, signal, band, security_status):
    score = 30
    breakdown = ["+ Base initialization score: +30"]

    # --- 1. Signal Strength ---
    if signal >= -55:
        score += 40
        breakdown.append(f"+ Excellent signal strength ({signal} dBm): +40")
    elif signal >= -67:
        score += 30
        breakdown.append(f"+ Good signal strength ({signal} dBm): +30")
    elif signal >= -75:
        score += 15
        breakdown.append(f"+ Fair signal strength ({signal} dBm): +15")
    else:
        score += 5
        breakdown.append(f"+ Weak signal strength ({signal} dBm): +5")

    # --- 2. WiFi Technology ---
    details_str = str(details)
    if "HE capabilities" in details_str:
        score += 15
        breakdown.append("+ Wi-Fi 6 (HE) support: +15")
    elif "VHT capabilities" in details_str:
        score += 10
        breakdown.append("+ Wi-Fi 5 (VHT) support: +10")
    elif "HT capabilities" in details_str:
        score += 5
        breakdown.append("+ Wi-Fi 4 (HT) support: +5")

    if band == "5GHz":
        score += 5
        breakdown.append("+ 5GHz Band (Lower interference): +5")

    # --- 3. Optimization Features ---
    ext_caps = str(details.get("Extended capabilities", ""))
    if "BSS Transition" in ext_caps:
        score += 5
        breakdown.append("+ Roaming support (BSS Transition): +5")

    vht_op = str(details.get("VHT operation", ""))
    if "80 MHz" in vht_op or "160 MHz" in vht_op:
        score += 5
        breakdown.append("+ High bandwidth (80/160 MHz): +5")

    # --- 4. Security Bonus ---
    if any(x in security_status for x in ["WPA3", "Enterprise", "MFP Protected"]):
        score += 10
        breakdown.append("+ Modern security standard (WPA3/Enterprise): +10")

    return score, breakdown


def evaluate_network_quality(details):
    """
    Evaluates the advantages and disadvantages of a WiFi network.
    """
    pros = []
    cons = []

    # --- 1. Signal Strength Assessment ---
    signal_str = details.get("signal", "-100").split()[0]
    try:
        signal = int(float(signal_str))
        if signal >= -50:
            pros.append("Excellent signal strength (Stable connection)")
        elif signal >= -67:
            pros.append("Good signal strength for most activities")
        elif signal <= -80:
            cons.append("Very weak signal (High risk of disconnection)")
        elif signal <= -75:
            cons.append("Poor signal strength (May cause lag/latency)")
    except (ValueError, IndexError):
        pass

    # --- 2. Frequency Band & Interference ---
    freq = float(details.get("freq", 0))
    if freq >= 5000:
        pros.append("5GHz Band: Higher data rates and less congestion")
    else:
        cons.append("2.4GHz Band: High interference from Bluetooth/Microwaves")

    # --- 3. WiFi Standards & Capabilities ---
    if "HE capabilities" in details:
        pros.append("WiFi 6 (802.11ax) supported: High efficiency")
    elif "VHT capabilities" in details:
        pros.append("WiFi 5 (802.11ac) supported: High speed performance")
    elif "HT capabilities" in details:
        pros.append("WiFi 4 (802.11n) supported")
    else:
        cons.append("Legacy standard (802.11a/b/g): Very slow throughput")

    # --- 4. Security Assessment (Sử dụng hàm evaluate_security) ---
    security_status = evaluate_security(details)

    # Phân loại dựa trên Risk Level trong chuỗi trả về
    if any(level in security_status for level in ["Critical", "High Risk"]):
        cons.append(f"Security Alert: {security_status}")
    elif "Medium Risk" in security_status:
        pros.append(f"Security: {security_status}")
    elif any(level in security_status for level in ["Low Risk", "Very Low Risk"]):
        pros.append(f"Secure: {security_status}")
    else:
        cons.append(f"Security Warning: {security_status}")

    if "[WPS Enabled" in security_status:
        cons.append(
            "Vulnerability: WPS is active (Susceptible to Pixie-Dust/Brute-force)"
        )

    if "MFP Protected" in security_status:
        pros.append("Enhanced Protection: Management Frame Protection (MFP) is active")

    if "AES" in security_status or "CCMP" in security_status:
        pros.append("Strong Encryption: Using AES/CCMP instead of legacy TKIP")

    # --- 5. Network Optimization Features ---
    ext_caps = details.get("Extended capabilities", {})
    # Handling both dict or list structure depending on your parser
    caps_str = str(ext_caps)
    if "BSS Transition" in caps_str:
        pros.append("802.11v (BSS Transition) supported: Better roaming")

    # --- 6. Channel Width ---
    vht_op = details.get("VHT operation", {})
    if "80 MHz" in str(vht_op):
        pros.append("Ultrawide 80MHz channel for maximum bandwidth")

    return {"pros": pros, "cons": cons}


def analyze_dashboard_stats(networks):
    """
    Phân tích danh sách networks để trả về các thông số hiển thị trên Dashboard
    và dữ liệu cấu trúc cho biểu đồ.
    """
    stats = {
        "total_aps": 0,
        "strong_security": 0,
        "weak_security": 0,
        "suspicious_aps": 0,
        # Thống kê chi tiết các cấp độ rủi ro (Risk Levels)
        "risk_dist": {
            "Very Low Risk": 0,
            "Low Risk": 0,
            "Medium Risk": 0,
            "High Risk": 0,
            "Critical": 0,
            "Unknown": 0,
        },
        # Thống kê chi tiết loại hình bảo mật (Security Types)
        "security_detailed": {
            "WPA3 Only": 0,
            "WPA2/WPA3 Mixed": 0,
            "WPA2 Only": 0,
            "WPA1/WPA2 Mixed": 0,
            "WPA1 Legacy": 0,
            "WEP": 0,
            "Open": 0,
            "Others": 0,
        },
        # Dữ liệu cho biểu đồ
        "freq_dist": {"2.4 GHz": 0, "5 GHz": 0, "6 GHz": 0},
        "signal_dist": {"Excellent": 0, "Good": 0, "Fair": 0, "Poor": 0},
        "security_detailed": defaultdict(
            int
        ),  # Phân loại chi tiết (WPA2, WPA3, Open...)
        "channel_dist": defaultdict(int),  # Mật độ thiết bị trên mỗi kênh
        "vendor_dist": defaultdict(int),  # Phân phối theo nhà sản xuất (OUI)
    }

    stats["total_aps"] = len(networks)

    for ap in networks:
        details = ap.get("details", {})

        # 1. Xử lý Bảo mật
        sec_label = evaluate_security(details)

        if "Very Low Risk" in sec_label:
            stats["risk_dist"]["Very Low Risk"] += 1
            stats["strong_security"] += 1
        elif "Low Risk" in sec_label:
            stats["risk_dist"]["Low Risk"] += 1
            stats["strong_security"] += 1
        elif "Medium Risk" in sec_label:
            stats["risk_dist"]["Medium Risk"] += 1
            stats["strong_security"] += 1
        elif "High Risk" in sec_label:
            stats["risk_dist"]["High Risk"] += 1
            stats["weak_security"] += 1
        elif "Critical" in sec_label:
            stats["risk_dist"]["Critical"] += 1
            stats["weak_security"] += 1
        else:
            stats["risk_dist"]["Unknown"] += 1

        # Phân loại cho biểu đồ dựa trên cấu trúc key
        if "WPA3-SAE Only" in sec_label:
            stats["security_detailed"]["WPA3 Only"] += 1
        elif "WPA3 Transition Mode" in sec_label:
            stats["security_detailed"]["WPA2/WPA3 Mixed"] += 1
        elif "Mixed WPA1/WPA2" in sec_label:
            stats["security_detailed"]["WPA1/WPA2 Mixed"] += 1
        elif "WPA2" in sec_label:
            # Bao gồm WPA2 AES, WPA2 TKIP, WPA2 Enterprise
            stats["security_detailed"]["WPA2 Only"] += 1
        elif "WPA1 Legacy" in sec_label:
            stats["security_detailed"]["WPA1 Legacy"] += 1
        elif "WEP" in sec_label:
            stats["security_detailed"]["WEP"] += 1
        elif "Open Network" in sec_label:
            stats["security_detailed"]["Open"] += 1
        else:
            stats["security_detailed"]["Others"] += 1

        # 2. Phân phối Băng tần (Frequency)
        try:
            freq = float(details.get("freq", 0))
            if 2400 <= freq < 3000:
                stats["freq_dist"]["2.4 GHz"] += 1
            elif 5000 <= freq < 6000:
                stats["freq_dist"]["5 GHz"] += 1
            elif freq >= 6000:
                stats["freq_dist"]["6 GHz"] += 1
        except:
            pass

        # 3. Phân phối Tín hiệu (Signal Strength)
        try:
            # Signal format: "-43.00 dBm"
            sig_raw = details.get("signal", "-100")
            sig_val = int(float(sig_raw.split()[0]))

            if sig_val >= -50:
                stats["signal_dist"]["Excellent"] += 1
            elif -60 <= sig_val < -50:
                stats["signal_dist"]["Good"] += 1
            elif -70 <= sig_val < -60:
                stats["signal_dist"]["Fair"] += 1
            else:
                stats["signal_dist"]["Poor"] += 1
        except:
            pass

        # 4. Phân phối Kênh (Channel)
        # Lấy từ "DS Parameter set" hoặc "primary channel"
        chan = details.get("DS Parameter set") or details.get("HT operation", {}).get(
            "primary channel"
        )
        if chan:
            stats["channel_dist"][str(chan)] += 1

        # 5. Phân phối Nhà sản xuất (Vendor OUI)
        bssid = ap.get("bssid", "").upper()
        if bssid and len(bssid) >= 8:
            oui = bssid[:8]  # Lấy 3 byte đầu
            stats["vendor_dist"][oui] += 1

    # 6. Đếm số lượng AP nghi vấn
    suspicious_results = detect_suspicious_networks(networks)
    total_suspicious_count = 0
    for item in suspicious_results:
        total_suspicious_count += item.get("ap_count", 0)
    stats["suspicious_aps"] = total_suspicious_count

    stats["security_detailed"] = dict(stats["security_detailed"])
    stats["channel_dist"] = dict(
        sorted(
            stats["channel_dist"].items(),
            key=lambda x: int(x[0]) if x[0].isdigit() else 0,
        )
    )
    stats["vendor_dist"] = dict(stats["vendor_dist"])

    return stats


def analyze_scan_table(networks):
    """Đưa ra dữ liệu hiển thị lên bảng"""
    analyzed_results = []

    for net in networks:
        details = net.get("details", {})

        # 1. SIGNAL & BARS
        signal_raw = details.get("signal", "-100.00 dBm")
        # Tìm số thực (có thể có dấu âm) trong chuỗi signal
        signal_match = re.search(r"-?\d+\.?\d*", signal_raw)
        signal_val = float(signal_match.group()) if signal_match else -100.0

        if signal_val <= -100:
            quality = 0
        elif signal_val >= -50:
            quality = 100
        else:
            quality = int(2 * (signal_val + 100))

        # Phân cấp Bar Level cho Icon (0-4)
        if quality > 80:
            bar_level = 4
        elif quality > 60:
            bar_level = 3
        elif quality > 40:
            bar_level = 2
        elif quality > 20:
            bar_level = 1
        else:
            bar_level = 0

        # 2. SECURITY
        security = evaluate_security(details)

        # 3. BAND
        freq_val = float(details.get("freq", 0))
        band = "5 GHz" if freq_val > 4000 else "2.4 GHz"

        # 4. CHANNEL
        ch_info = details.get("DS Parameter set", "")
        ch_match = re.search(r"\d+", ch_info)
        channel = ch_match.group() if ch_match else "?"

        # 5. SSID
        ssid = details.get("SSID", "")
        if not ssid:  # Xử lý mạng ẩn
            ssid = "<Hidden Network>"

        row = {
            "in_use": net.get("associated", False),
            "ssid": ssid,
            "bssid": net.get("bssid", "").upper(),
            "signal": f"{quality}%",
            "bar_level": bar_level,
            "channel": channel,
            "band": band,
            "security": security,
        }
        analyzed_results.append(row)

    return analyzed_results
