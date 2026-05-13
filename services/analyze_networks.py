from services.scan_networks import detect_suspicious_networks, evaluate_security
import re


def process_security_analysis(details, security_status, suspicious_data):
    """
    Unified security analysis: Includes specific evaluations for Mixed Mode configurations.
    """
    score = 80  # Base score for a standard WPA2-PSK (AES Only) network
    score_breakdown = []
    pros = []
    cons = []
    score_breakdown.append(f"Base score: {score}")

    all_info = str(details).upper()
    ssid = details.get("SSID", "")

    # 1. CRITICAL FAILURES (Immediate 0 Score)
    if "Open Network" in security_status or "WEP" in security_status:
        score = 0
        score_breakdown.append("Critical: Unencrypted or WEP network detected (0pts)")
        cons.append(
            "Unencrypted network: Data transmission is fully visible to attackers."
        )
        return score, score_breakdown, pros, cons

    if suspicious_data:
        score = 0
        score_breakdown.append("Critical: Rogue AP / Evil Twin detected! (0pts)")
        cons.append(
            "Rogue AP indicator: This access point is likely spoofed or malicious."
        )
        return score, score_breakdown, pros, cons

    # 2. PROTOCOL & MIXED MODE EVALUATION
    # Case A: WPA3 SAE (Pure or Transition)
    if "WPA3" in security_status:
        if "Transition" in security_status or "Mixed" in security_status:
            score += 5
            score_breakdown.append("WPA2/WPA3 Mixed Mode (Transition) detected (+5pts)")
            pros.append(
                "WPA3 Support: Provides enhanced security for compatible modern devices."
            )
            cons.append(
                "Mixed Mode: Maintains WPA2 compatibility, which may allow downgrade attacks."
            )
        else:
            score += 20  # Premium score for pure WPA3
            score_breakdown.append("Pure WPA3-SAE encryption (+20pts)")
            pros.append(
                "Pure WPA3-SAE: Highest security standard with mandatory protection features."
            )

    # Case B: WPA1/WPA2 Mixed
    elif "Mixed" in security_status and "WPA1" in security_status:
        score -= 30
        score_breakdown.append("Legacy Mixed Mode (WPA1/WPA2) detected (-30pts)")
        cons.append(
            "Legacy Mixed Mode: Compromises security by supporting outdated WPA1 protocols."
        )

    # Case C: Pure Legacy WPA1
    elif "WPA1" in security_status and "WPA2" not in security_status:
        score -= 50
        score_breakdown.append("Legacy WPA1 protocol only (-50pts)")
        cons.append("Legacy WPA1: Highly vulnerable and obsolete encryption protocol.")

    # 3. CIPHER ANALYSIS (TKIP vs AES)
    if "TKIP" in security_status:
        score -= 20
        score_breakdown.append("Weak TKIP cipher detected (-20pts)")
        cons.append(
            "Weak TKIP cipher: Outdated encryption susceptible to packet decryption."
        )
    elif "AES" in all_info or "CCMP" in all_info:
        pros.append(
            "Strong AES/CCMP encryption: The current industry standard for data privacy."
        )

    # 4. AUTHENTICATION BONUSES
    if "802.1X" in all_info or "EAP" in all_info:
        score += 15
        score_breakdown.append("Enterprise-grade 802.1X authentication (+15pts)")
        pros.append(
            "802.1X Enterprise: Strongest authentication method using individual credentials."
        )
    else:
        score -= 5
        score_breakdown.append("Personal PSK authentication (-5pts)")
        cons.append(
            "Personal PSK: Vulnerable to offline dictionary and brute-force attacks."
        )

    # 5. SECURITY FEATURE BONUSES / PENALTIES
    # WPS Vulnerability
    if "WPS" in details or "WI-FI PROTECTED SETUP" in all_info:
        score -= 30
        score_breakdown.append("Vulnerable WPS protocol enabled (-30pts)")
        cons.append(
            "WPS enabled: Vulnerable to PIN brute-force attacks (e.g., Reaver/Bully)."
        )

    # Management Frame Protection (MFP)
    if "MFP-REQUIRED" in all_info:
        score += 10
        score_breakdown.append("Strict MFP Requirement (+10pts)")
        pros.append("Strict MFP: Protects all management frames from being spoofed.")
    elif "MFP-CAPABLE" in all_info:
        score += 5
        score_breakdown.append("MFP Capable (+5pts)")
        pros.append(
            "MFP Capable: Offers protection for management frames if supported by clients."
        )
    else:
        score -= 10
        score_breakdown.append("MFP missing (-10pts)")
        cons.append(
            "Missing MFP: Vulnerable to targeted de-authentication (disconnection) attacks."
        )

    # 6. CONFIGURATION ISSUES
    if not ssid or "\\x00" in ssid or "<length: 0>" in ssid:
        score -= 10
        score_breakdown.append("Hidden SSID detected (-10pts)")
        cons.append(
            "Hidden SSID: Leaks device information through constant probe requests."
        )

    # 7. PERFORMANCE METADATA (Pros/Cons Only)
    try:
        freq = float(str(details.get("freq", "0")).split()[0])
        signal = float(str(details.get("signal", "0")).split()[0])
        if freq > 4000:
            pros.append(
                "5GHz Band: Higher bandwidth and lower interference than 2.4GHz."
            )
        if signal > -50 and signal != 0:
            pros.append("Excellent signal: High connection stability and SNR.")
        elif signal < -80 and signal != 0:
            cons.append(
                "Weak signal: Unreliable connection might risk session hijacking."
            )
    except:
        pass

    # Final Score Normalization
    score = max(0, min(100, score))

    return score, score_breakdown, pros, cons


def analyze_network(target_bssid, networks):
    """
    Main analysis function for a specific network.
    """
    target_bssid = target_bssid.lower()
    net = next(
        (n for n in networks if n.get("bssid", "").lower() == target_bssid), None
    )

    if not net:
        return None

    details = net.get("details", {})
    ssid = details.get("SSID", "Unknown")

    # Step 1: Security Diagnosis
    security_status = evaluate_security(details)

    # Step 2: Rogue AP Check
    try:
        suspicious_list = detect_suspicious_networks(networks)
    except:
        suspicious_list = []

    suspicious_data = next(
        (item for item in suspicious_list if item["bssid"].lower() == target_bssid),
        None,
    )

    # Step 3: Scoring & Detail Evaluation
    final_score, score_breakdown, pros, cons = process_security_analysis(
        details, security_status, suspicious_data
    )

    # Basic Metadata collection
    try:
        freq_str = details.get("freq", "0")
        freq = float(str(freq_str).split()[0])
    except:
        freq = 0

    band = "5GHz" if freq > 4000 else "2.4GHz"
    channel = details.get("DS Parameter set", "N/A")
    signal_raw = details.get("signal", "N/A")
    signal = signal_raw.split()[0] if " " in str(signal_raw) else signal_raw

    # Return structure maintained as requested
    return {
        "SSID": ssid,
        "BSSID": target_bssid.upper(),
        "Security": security_status,
        "Band": band,
        "Channel": channel,
        "Signal": signal,
        "Score": final_score,
        "ScoreBreakdown": score_breakdown,
        "Pros": pros,
        "Cons": cons,
        "IsRogue": True if suspicious_data else False,
        "Details": details,
    }


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
