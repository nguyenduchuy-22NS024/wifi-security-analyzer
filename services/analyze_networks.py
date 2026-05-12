from services.scan_networks import detect_suspicious_networks, evaluate_security
import re


def analyze_network(target_bssid, networks):
    target_bssid = target_bssid.lower()
    net = next(
        (n for n in networks if n.get("bssid", "").lower() == target_bssid), None
    )

    if not net:
        return None

    details = net.get("details", {})
    ssid = details.get("SSID", "Unknown")

    # --- Bước 1: Chẩn đoán Bảo mật (Dùng hàm của bạn) ---
    security_status = evaluate_security(details)

    # --- Bước 2: Kiểm tra dấu hiệu giả mạo (Rogue AP) ---
    # Giả định bạn đã có hàm detect_suspicious_networks
    suspicious_list = detect_suspicious_networks(networks)
    suspicious_data = next(
        (item for item in suspicious_list if item["bssid"].lower() == target_bssid),
        None,
    )

    # --- Bước 3: Tính điểm & Đánh giá (Module mới) ---
    final_score, score_breakdown = calculate_security_score(
        details, security_status, suspicious_data
    )
    analysis = evaluate_security_pros_cons(details, security_status, suspicious_data)

    # Thu thập metadata cơ bản
    freq = float(details.get("freq", 0))
    band = "5GHz" if freq > 4000 else "2.4GHz"
    channel = details.get("DS Parameter set", "N/A")
    signal = details.get("signal", "N/A")

    return {
        "SSID": ssid,
        "BSSID": target_bssid.upper(),
        "Security": security_status,
        "Band": band,
        "Channel": channel,
        "Signal": signal,
        "Score": final_score,
        "ScoreBreakdown": score_breakdown,
        "Pros": analysis["pros"],
        "Cons": analysis["cons"],
        "IsRogue": True if suspicious_data else False,
        "Details": details,
    }


def calculate_security_score(details, security_status, suspicious_data):
    """
    Tính điểm tập trung hoàn toàn vào bảo mật.
    Thang điểm 100.
    """
    score = 100
    breakdown = []

    # --- 1. Đánh giá dựa trên chuẩn mã hóa (Từ hàm evaluate_security) ---
    if "Critical" in security_status:
        score = 10
        breakdown.append(
            f"+ CRITICAL: Protocol is severely flawed ({security_status}): 10pts"
        )
    elif "High Risk" in security_status:
        score = 40
        breakdown.append(
            f"+ HIGH RISK: Legacy or mixed encryption ({security_status}): 40pts"
        )
    elif "Medium Risk" in security_status:
        score = 70
        breakdown.append(f"+ MEDIUM RISK: Standard protection ({security_status}): 70pts")
    elif "Low Risk" in security_status or "Very Low Risk" in security_status:
        score = 95
        breakdown.append(f"+ SECURE: Modern encryption ({security_status}): 95pts")
        if "WPA3" in security_status:
            score = 100
            breakdown.append("+ BONUS: Cutting-edge WPA3 protection: 5pts")

    # --- 2. Hình phạt bổ sung (Vulnerabilities) ---
    # WPS là lỗ hổng cực nghiêm trọng
    if "WPS Enabled" in security_status:
        score -= 40
        breakdown.append(
            "- VULNERABILITY: WPS Enabled (Pixie-Dust/Brute-force risk): -40pts"
        )

    # Management Frame Protection (MFP)
    if "MFP Protected" not in security_status and score > 20:
        score -= 10
        breakdown.append(
            "- WARNING: MFP not active (Vulnerable to De-auth attacks): -10pts"
        )

    # Hidden SSID (Không tăng bảo mật, chỉ gây rối)
    if details.get("SSID") == "" or "length: 0" in str(details):
        score -= 5
        breakdown.append("- INFO: Hidden SSID (Ineffective security-by-obscurity): 5pts")

    # --- 3. Hình phạt từ hệ thống phát hiện Rogue AP ---
    if suspicious_data:
        risk_lvl = suspicious_data["risk_level"]
        if risk_lvl == "CRITICAL":
            score = 0
            breakdown.append(
                "- ALERT: Confirmed Rogue AP/Evil Twin detected: SCORE RESET TO 0"
            )
        elif risk_lvl == "HIGH":
            score -= 50
            breakdown.append(
                "- ALERT: Highly suspicious activity (MAC Spoofing?): -50pts"
            )

    # Tín hiệu quá mạnh (Nghi vấn AP giả ngay cạnh)
    try:
        signal = int(float(details.get("signal", "-100").split()[0]))
        if signal > -25:
            score -= 15
            breakdown.append(
                f"- WARNING: Signal too strong ({signal} dBm), potential Evil Twin: -15pts"
            )
    except:
        pass

    final_score = max(0, min(100, score))
    return final_score, breakdown


def evaluate_security_pros_cons(details, security_status, suspicious_data):
    pros = []
    cons = []

    # Phân tích từ security_status
    if "WPA3" in security_status:
        pros.append(
            "Modern Encryption: WPA3 (SAE) provides robust protection against offline dictionary attacks"
        )
    if "Enterprise" in security_status:
        pros.append(
            "Enterprise Auth: 802.1X provides individual credentials, increasing accountability"
        )
    if "MFP Protected" in security_status:
        pros.append(
            "Anti-Deauth: Management Frame Protection (MFP) prevents forced disconnections"
        )
    if "AES" in security_status or "CCMP" in security_status:
        pros.append(
            "Strong Cipher: CCMP/AES is a secure, hardware-accelerated encryption method"
        )

    # Phân tích nhược điểm
    if "Critical" in security_status or "Open" in security_status:
        cons.append("CRITICAL: Network is unencrypted. Anyone can sniff your traffic")
    if "WPS Enabled" in security_status:
        cons.append(
            "VULNERABILITY: WPS is ON. Attackers can recover your password via PIN brute-force"
        )
    if "TKIP" in security_status:
        cons.append(
            "Legacy Cipher: TKIP is deprecated and vulnerable to decryption attacks"
        )

    # Rogue AP
    if suspicious_data:
        cons.append(
            f"SPOOFING ALERT: This AP matches a known SSID but has suspicious characteristics ({suspicious_data['risk_level']})"
        )
        for reason in suspicious_data.get("reasons", []):
            cons.append(f"Risk Factor: {reason}")

    # Tín hiệu & Vật lý
    try:
        signal = int(float(details.get("signal", "-100").split()[0]))
        if signal < -80:
            cons.append(
                "DoS Risk: Signal is too weak, easily disrupted by noise or intentional jamming"
            )
    except:
        pass

    return {"pros": pros, "cons": cons}


def analyze_dashboard_stats(networks):
    stats = {
        "total_aps": len(networks),
        "strong_security": 0,
        "weak_security": 0,
        "suspicious_aps": 0,
        # 1. Biểu đồ: Mức độ rủi ro
        "risk_dist": {
            "Very Low Risk": 0,
            "Low Risk": 0,
            "Medium Risk": 0,
            "High Risk": 0,
            "Critical": 0,
            "Unknown": 0,
        },
        # 2. Biểu đồ: Chi tiết chuẩn bảo mật (Ví dụ: WPA3, WPA2...)
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
        # 3. Biểu đồ mới: Phân phối Cipher (Mã hóa luồng - Rất quan trọng trong bảo mật)
        "cipher_dist": {
            "AES/CCMP (Strong)": 0,
            "TKIP (Weak/Legacy)": 0,
            "Mixed (AES+TKIP)": 0,
            "No Encryption": 0,
        },
        # 4. Biểu đồ mới: Trạng thái WPS (Lỗ hổng cực lớn)
        "wps_dist": {"WPS Enabled (Vulnerable)": 0, "WPS Disabled/Hidden": 0},
        # 5. Biểu đồ mới: Management Frame Protection (MFP - Chống tấn công ngắt kết nối)
        "mfp_dist": {"MFP Required": 0, "MFP Capable": 0, "No MFP": 0},
        # 6. Biểu đồ mới: Loại hình xác thực
        "auth_dist": {"Personal (PSK)": 0, "Enterprise (802.1X)": 0, "None (Open)": 0},
    }

    for ap in networks:
        details = ap.get("details", {})
        all_info_str = str(details).upper()

        # --- A. ĐÁNH GIÁ RỦI RO & CHUẨN BẢO MẬT ---
        sec_label = evaluate_security(details)

        # Cập nhật risk_dist và strong/weak stats
        if "Very Low" in sec_label:
            stats["risk_dist"]["Very Low Risk"] += 1
            stats["strong_security"] += 1
        elif "Low Risk" in sec_label:
            stats["risk_dist"]["Low Risk"] += 1
            stats["strong_security"] += 1
        elif "Medium" in sec_label:
            stats["risk_dist"]["Medium Risk"] += 1
            stats["strong_security"] += 1
        elif "High" in sec_label:
            stats["risk_dist"]["High Risk"] += 1
            stats["weak_security"] += 1
        elif "Critical" in sec_label:
            stats["risk_dist"]["Critical"] += 1
            stats["weak_security"] += 1
        else:
            stats["risk_dist"]["Unknown"] += 1

        # Cập nhật security_detailed
        if "WPA3-SAE Only" in sec_label:
            stats["security_detailed"]["WPA3 Only"] += 1
        elif "WPA3 Transition" in sec_label:
            stats["security_detailed"]["WPA2/WPA3 Mixed"] += 1
        elif "Mixed WPA1/WPA2" in sec_label:
            stats["security_detailed"]["WPA1/WPA2 Mixed"] += 1
        elif "WPA2" in sec_label:
            stats["security_detailed"]["WPA2 Only"] += 1
        elif "WPA1" in sec_label:
            stats["security_detailed"]["WPA1 Legacy"] += 1
        elif "WEP" in sec_label:
            stats["security_detailed"]["WEP"] += 1
        elif "Open" in sec_label:
            stats["security_detailed"]["Open"] += 1
        else:
            stats["security_detailed"]["Others"] += 1

        # --- B. PHÂN TÍCH CIPHER (MÃ HÓA LUỒNG) ---
        has_ccmp = "CCMP" in all_info_str or "AES" in all_info_str
        has_tkip = "TKIP" in all_info_str
        if "PRIVACY" not in str(details.get("capability", "")).upper():
            stats["cipher_dist"]["No Encryption"] += 1
        elif has_ccmp and has_tkip:
            stats["cipher_dist"]["Mixed (AES+TKIP)"] += 1
        elif has_tkip:
            stats["cipher_dist"]["TKIP (Weak/Legacy)"] += 1
        elif has_ccmp:
            stats["cipher_dist"]["AES/CCMP (Strong)"] += 1

        # --- C. PHÂN TÍCH WPS ---
        if "WPS" in details or "WI-FI PROTECTED SETUP" in all_info_str:
            stats["wps_dist"]["WPS Enabled (Vulnerable)"] += 1
        else:
            stats["wps_dist"]["WPS Disabled/Hidden"] += 1

        # --- D. PHÂN TÍCH MFP (BẢO VỆ KHUNG QUẢN LÝ) ---
        if "MFP-REQUIRED" in all_info_str:
            stats["mfp_dist"]["MFP Required"] += 1
        elif "MFP-CAPABLE" in all_info_str:
            stats["mfp_dist"]["MFP Capable"] += 1
        else:
            stats["mfp_dist"]["No MFP"] += 1

        # --- E. PHÂN TÍCH LOẠI HÌNH XÁC THỰC ---
        if "802.1X" in all_info_str or "EAP" in all_info_str:
            stats["auth_dist"]["Enterprise (802.1X)"] += 1
        elif "PSK" in all_info_str or "SAE" in all_info_str:
            stats["auth_dist"]["Personal (PSK)"] += 1
        else:
            stats["auth_dist"]["None (Open)"] += 1

    # 6. Đếm số lượng AP nghi vấn
    try:
        suspicious_results = detect_suspicious_networks(networks)
        stats["suspicious_aps"] = sum(
            item.get("ap_count", 0) for item in suspicious_results
        )
    except:
        stats["suspicious_aps"] = 0

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
