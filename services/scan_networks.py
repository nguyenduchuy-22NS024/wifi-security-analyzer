import subprocess, re, json
from collections import defaultdict


def get_network_interfaces():
    """Lấy danh sách các interface WiFi khả dụng."""
    interfaces = []
    try:
        cmd = subprocess.run(["iw", "dev"], capture_output=True, text=True, check=True)
        for line in cmd.stdout.splitlines():
            if "Interface" in line:
                ifname = line.split()[1]
                interfaces.append(ifname)
    except Exception as e:
        print(f"Error getting interfaces: {e}")
    return interfaces


def scan_networks(interface: str):
    """Quét toàn WiFi xung quanh"""
    networks = []
    cmd = subprocess.run(
        ["iw", "dev", interface, "scan"], capture_output=True, text=True, check=True
    )

    if cmd.returncode != 0:
        return []

    raw_data = cmd.stdout.strip()
    if not raw_data:
        return []

    bss_list = re.split(r"\n(?=BSS\s)", "\n" + raw_data)
    for raw_bss in bss_list:
        if raw_bss.strip():
            networks.append(parse_raw_bss(raw_bss))

    return networks


def parse_raw_bss(raw_data):

    def clean_text(text):
        if not text:
            return ""
        text = re.sub(r"^[\s\*]+", "", text)  # Xóa khoảng trắng và dấu *
        return text.replace("\t", " ").strip()

    lines = raw_data.split("\n")
    header = lines[0]
    interface_match = re.search(r"on\s+([^\s\)]+)", header)
    bssid_match = re.search(r"BSS\s+([0-9a-f:]{17})", header)
    bss = {
        "bssid": bssid_match.group(1) if bssid_match else None,
        "interface": interface_match.group(1) if interface_match else None,
        "associated": "associated" in header,
        "details": {},
    }
    # Stack saves (indentation, current dictionary)
    stack = [(-1, bss["details"])]
    all_lines = [l for l in lines[1:] if l.strip()]
    for i, line in enumerate(all_lines):
        indent = len(line) - len(line.lstrip())
        content = clean_text(line)
        # Check if the next line has a deeper indent than this line.
        has_children = False
        if i + 1 < len(all_lines):
            next_indent = len(all_lines[i + 1]) - len(all_lines[i + 1].lstrip())
            if next_indent > indent:
                has_children = True
        while stack and indent <= stack[-1][0]:
            stack.pop()
        current_node = stack[-1][1]
        if ":" in content:
            parts = content.split(":", 1)
            key = clean_text(parts[0])
            val = clean_text(parts[1])
            # If you have children or special WPA/RSN/Country entries
            if has_children or key in ["WPA", "RSN", "Country"] or not val:
                new_node = {}
                # Handle accompanying content (such as Country: US or WPA: Version 1)
                if val:
                    if "Environment" in val:  # Only Country
                        env = val.split("Environment:", 1)
                        new_node["Code"] = clean_text(env[0])
                        new_node["Environment"] = clean_text(env[1])
                    elif ":" in val:
                        sub = val.split(":", 1)
                        new_node[clean_text(sub[0])] = clean_text(sub[1])
                    else:
                        new_node["info"] = val
                current_node[key] = new_node
                stack.append((indent, new_node))
            else:
                # Key-Value
                if key in current_node:
                    if not isinstance(current_node[key], list):
                        current_node[key] = [current_node[key]]
                    current_node[key].append(val)
                else:
                    current_node[key] = val
        else:
            # Flags or lines without colons ':'
            target_key = "constraints" if "Code" in current_node else "flags"
            if target_key not in current_node:
                current_node[target_key] = []
            current_node[target_key].append(content)

    return bss


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
        score = 0

        # --- Rule 1: Security Mismatch (Trọng số cao nhất: 80đ) ---
        securities = set()
        for ap in aps:
            dtl = ap.get("details", {})
            sec_type = "Open"
            if "RSN" in dtl or "WPA" in dtl:
                sec_type = "Encrypted"
            securities.add(sec_type)

        if len(securities) > 1:
            reasons.append(
                "Security mismatch (Found Open and Encrypted APs with same SSID)"
            )
            score += 80

        # --- Rule 2: 5G SSID on 2.4GHz Frequency (Trọng số: 60đ) ---
        # Tên mạng ghi 5G nhưng tần số phát lại là 2.4GHz (dấu hiệu lừa đảo kỹ thuật).
        freq_anomaly = False
        for ap in aps:
            try:
                freq = float(ap.get("details", {}).get("freq", 0))
                if "5G" in ssid.upper() and freq < 3000:
                    freq_anomaly = True
                    break
            except:
                pass
        if freq_anomaly:
            reasons.append("Frequency anomaly (5G SSID detected on 2.4GHz band)")
            score += 60

        # --- Rule 3: Capability/Standard Mismatch (Trọng số: 40đ) ---
        # Một AP dùng WiFi 6 (HE), một AP cùng tên chỉ dùng WiFi 4 (HT).
        standards = set()
        for ap in aps:
            dtl = ap.get("details", {})
            if "HE capabilities" in dtl:
                standards.add("WiFi 6")
            elif "VHT capabilities" in dtl:
                standards.add("WiFi 5")
            elif "HT capabilities" in dtl:
                standards.add("WiFi 4")

        if len(standards) > 1:
            reasons.append(f"Hardware capability mismatch: {list(standards)}")
            score += 40

        # --- Rule 4: Vendor (OUI) Mismatch (Trọng số: 30đ) ---
        # Các hệ thống Mesh doanh nghiệp thường dùng cùng 1 hãng thiết bị.
        ouis = set(ap["bssid"].upper()[:8] for ap in aps)
        if len(ouis) > 1:
            reasons.append(f"Vendor mismatch (Multiple manufacturers: {list(ouis)})")
            score += 30

        # --- Rule 5: TSF Anomaly - Uptime (Trọng số: 25đ) ---
        # AP mới dựng (giả mạo) có thời gian hoạt động cực thấp so với AP thật.
        tsf_values = []
        for ap in aps:
            try:
                tsf = ap.get("details", {}).get("TSF", "").split()[0]
                if tsf:
                    tsf_values.append(int(tsf))
            except:
                pass
        if len(tsf_values) > 1:
            diff_days = (max(tsf_values) - min(tsf_values)) / (10**6 * 3600 * 24)
            if diff_days > 10:  # Chênh lệch trên 10 ngày
                reasons.append(f"Significant uptime difference ({diff_days:.1f} days)")
                score += 25

        # --- Rule 6: Country Code Mismatch (Trọng số: 15đ) ---
        countries = set(
            ap.get("details", {}).get("Country", {}).get("Code") for ap in aps
        )
        countries.discard(None)
        if len(countries) > 1:
            reasons.append(f"Regulatory domain mismatch: {countries}")
            score += 15

        # Giới hạn điểm tối đa là 100
        final_score = min(100, score)

        # Phân loại rủi ro theo thang điểm 100
        if final_score > 0:
            risk_level = "Informational"
            if final_score >= 85:
                risk_level = "CRITICAL"
            elif final_score >= 60:
                risk_level = "HIGH"
            elif final_score >= 30:
                risk_level = "MEDIUM"
            else:
                risk_level = "LOW"

            suspicious_results.append(
                {
                    "ssid": ssid,
                    "risk_level": risk_level,
                    "risk_score": final_score,
                    "reasons": reasons,
                    "ap_count": len(aps),
                    "details": [
                        {
                            "bssid": a["bssid"],
                            "freq": a.get("details", {}).get("freq"),
                            "signal": a.get("details", {}).get("signal"),
                            "vendor_oui": a["bssid"].upper()[:8],
                        }
                        for a in aps
                    ],
                }
            )

    # Sắp xếp kết quả theo điểm số giảm dần
    return sorted(suspicious_results, key=lambda x: x["risk_score"], reverse=True)


def evaluate_security(details):
    """
    Hàm đánh giá bảo mật nâng cao: Phân biệt rõ Only, Mixed và Transition modes.
    Dựa trên sự hiện diện của các IE (Information Elements) trong gói tin Beacon/Probe.
    """
    # 1. Thu thập thông tin gốc
    rsn_raw = details.get("RSN", {})
    wpa_raw = details.get("WPA", {})  # WPA Version 1
    cap_info = str(details.get("capability", "")).upper()

    # Chuyển thành chuỗi để quét keyword nhanh
    rsn_str = str(rsn_raw).upper()
    wpa_str = str(wpa_raw).upper()
    all_info = (rsn_str + wpa_str + str(details.get("WPS", "")) + cap_info).upper()

    # 2. Các cờ nhận diện (Boolean flags)
    has_rsn = "RSN" in details  # Có block WPA2/WPA3
    has_wpa1 = "WPA" in details  # Có block WPA1
    is_sae = "SAE" in rsn_str  # Có chuẩn WPA3
    is_psk = "PSK" in all_info
    is_ent = any(x in all_info for x in ["802.1X", "EAP", "IEEE8021X"])

    has_tkip = "TKIP" in all_info
    has_ccmp = "CCMP" in all_info or "AES" in all_info

    has_wps = "WPS" in details or "WI-FI PROTECTED SETUP" in all_info
    has_mfp = "MFP-CAPABLE" in all_info or "MFP-REQUIRED" in all_info

    # Phụ gia thông tin
    wps_info = " [WPS Enabled - Vulnerable]" if has_wps else ""
    mfp_info = " (MFP Protected)" if has_mfp else ""

    # 3. LOGIC PHÂN LOẠI (Theo thứ tự từ hiện đại nhất đến cũ nhất)

    # --- TRƯỜNG HỢP KHÔNG CÓ MÃ HÓA HIỆN ĐẠI ---
    if "PRIVACY" not in cap_info:
        return "Critical (Open Network - No Encryption)"

    if not has_rsn and not has_wpa1:
        # Có Privacy nhưng không có RSN/WPA => Khả năng cao là WEP
        return f"Critical (WEP - Broken Security){wps_info}"

    # --- TRƯỜNG HỢP WPA3 (SAE) ---
    if is_sae:
        # Nếu có cả PSK (WPA2) hoặc có WPA1 block => Transition Mode
        if is_psk or has_wpa1:
            return f"Low-Medium Risk (WPA3 Transition Mode){mfp_info}{wps_info}"
        return f"Very Low Risk (WPA3-SAE Only){mfp_info}{wps_info}"

    # --- TRƯỜNG HỢP WPA1/WPA2 MIXED ---
    # Phải có cả 2 khối dữ liệu RSN và WPA trong Probe Response
    if has_rsn and has_wpa1:
        if has_tkip:
            return f"Critical (Mixed WPA1/WPA2 + TKIP){wps_info}"
        return f"High Risk (Mixed WPA1/WPA2 AES){wps_info}"

    # --- TRƯỜNG HỢP WPA2 ONLY (RSN ONLY) ---
    if has_rsn:
        if is_ent:
            return f"Low Risk (WPA2 Enterprise){mfp_info}{wps_info}"

        # Kiểm tra Cipher bên trong WPA2
        if has_tkip and not has_ccmp:
            return f"Critical (WPA2 with TKIP Only){wps_info}"
        if has_tkip and has_ccmp:
            # WPA2 cho phép cả AES và TKIP (thường thấy ở router cũ)
            return f"High Risk (WPA2 TKIP/AES Mixed){wps_info}"

        # Chuẩn an toàn phổ biến nhất hiện nay
        return f"Medium Risk (WPA2-PSK AES){mfp_info}{wps_info}"

    # --- TRƯỜNG HỢP WPA1 ONLY ---
    if has_wpa1:
        return f"High Risk (WPA1 Legacy){wps_info}"

    return f"Unknown Security (Manual Check Required){wps_info}"


# networks = scan_networks("wlp1s0")
# print(detect_suspicious_networks(networks))
