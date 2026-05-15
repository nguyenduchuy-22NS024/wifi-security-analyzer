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

        # Gom nhóm theo tiền tố MAC (4 cặp đầu) để xác định các cụm AP vật lý "họ hàng"
        mac_clusters = defaultdict(list)
        for ap in aps:
            prefix = ":".join(ap["bssid"].upper().split(":")[:4])
            mac_clusters[prefix].append(ap)

        # Baseline: Tìm đặc điểm chung của số đông AP trong SSID này (giả định là mạng thật)
        # 1. Vendor phổ biến nhất
        vendor_counts = defaultdict(int)
        for ap in aps:
            vendor_counts[ap["bssid"].upper()[:8]] += 1
        common_vendor = max(vendor_counts, key=vendor_counts.get)

        # 2. Capabilities phổ biến nhất (Dấu vân tay phần cứng)
        cap_counts = defaultdict(int)
        for ap in aps:
            dtl = ap.get("details", {})
            # Tạo một chuỗi định danh phần cứng từ các hex capabilities
            hw_sig = (
                f"HT:{dtl.get('HT capabilities', {}).get('Capabilities', 'None')}|"
                f"VHT:{dtl.get('VHT capabilities', {}).get('VHT Capabilities (hex)', 'None')}|"
                f"HE:{dtl.get('HE capabilities', {}).get('HE MAC Capabilities', 'None')}"
            )
            cap_counts[hw_sig] += 1
        common_hw_sig = max(cap_counts, key=cap_counts.get)

        # Duyệt từng AP để tính điểm nghi vấn (Anomaly Detection)
        for target_ap in aps:
            reasons = []
            score = 0
            dtl = target_ap.get("details", {})
            bssid = target_ap["bssid"].upper()

            # --- Rule 1: Security Mismatch (80đ) ---
            # Nếu AP này là Open trong khi số đông là Encrypted
            is_open = "RSN" not in dtl and "WPA" not in dtl
            has_encrypted_peers = any(
                ("RSN" in a.get("details", {}) or "WPA" in a.get("details", {}))
                for a in aps
                if a != target_ap
            )
            if is_open and has_encrypted_peers:
                reasons.append(
                    "Security Mismatch: AP is OPEN while others are Encrypted"
                )
                score += 80

            # --- Rule 2: MAC Spoofing Detection - HW Sig (70đ) ---
            # Dù MAC có thể giả mạo, nhưng Hex Capabilities của chipset rất khó giả mạo giống hệt
            target_hw_sig = (
                f"HT:{dtl.get('HT capabilities', {}).get('Capabilities', 'None')}|"
                f"VHT:{dtl.get('VHT capabilities', {}).get('VHT Capabilities (hex)', 'None')}|"
                f"HE:{dtl.get('HE capabilities', {}).get('HE MAC Capabilities', 'None')}"
            )
            if target_hw_sig != common_hw_sig and len(cap_counts) > 1:
                reasons.append(f"Hardware Signature Mismatch (Possible MAC Spoofing)")
                score += 70

            # --- Rule 3: Signal Strength Anomaly (60đ) ---
            # Tín hiệu quá mạnh thường là do kẻ giả mạo ngồi ngay cạnh nạn nhân
            try:
                sig_val = float(dtl.get("signal", "0").split()[0])
                if sig_val > -30:
                    reasons.append(
                        f"Signal strength anomaly ({sig_val} dBm) - Device very close"
                    )
                    score += 60
            except:
                pass

            # --- Rule 4: TSF Anomaly - Uptime (50đ) ---
            # Nếu AP này có uptime cực thấp trong khi cụm MAC "họ hàng" có uptime cực cao
            try:
                target_tsf = int(dtl.get("TSF", "0").split()[0])
                peer_tsfs = [
                    int(a.get("details", {}).get("TSF", "0").split()[0])
                    for a in aps
                    if a != target_ap
                ]
                if peer_tsfs and target_tsf < max(peer_tsfs) / 100:  # Thấp hơn 100 lần
                    reasons.append(
                        "TSF Anomaly: Uptime is significantly lower than peers"
                    )
                    score += 50
            except:
                pass

            # --- Rule 5: Vendor Mismatch (40đ) ---
            if bssid[:8] != common_vendor:
                reasons.append(f"Vendor Mismatch: {bssid[:8]} (Main: {common_vendor})")
                score += 40

            # --- Rule 6: Information Elements Inconsistency (30đ) ---
            # Kiểm tra Country Code và BSS Color
            target_cc = dtl.get("Country", {}).get("Code")
            target_color = dtl.get("HE Operation", {}).get("BSS Color")

            # Lấy CC và Color phổ biến nhất trong nhóm
            all_cc = [
                a.get("details", {}).get("Country", {}).get("Code")
                for a in aps
                if a.get("details", {}).get("Country", {}).get("Code")
            ]
            all_color = [
                a.get("details", {}).get("HE Operation", {}).get("BSS Color")
                for a in aps
                if a.get("details", {}).get("HE Operation", {}).get("BSS Color")
            ]

            if all_cc and target_cc and target_cc != max(set(all_cc), key=all_cc.count):
                reasons.append(f"Country Code mismatch: {target_cc}")
                score += 30
            if (
                all_color
                and target_color
                and target_color != max(set(all_color), key=all_color.count)
            ):
                reasons.append(f"BSS Color mismatch: {target_color}")
                score += 20

            # --- Tổng hợp kết quả cho từng AP nghi vấn ---
            final_score = min(100, score)
            if final_score >= 30:
                risk_level = "LOW"
                if final_score >= 85:
                    risk_level = "CRITICAL"
                elif final_score >= 60:
                    risk_level = "HIGH"
                elif final_score >= 40:
                    risk_level = "MEDIUM"

                suspicious_results.append(
                    {
                        "ssid": ssid,
                        "bssid": target_ap["bssid"],
                        "risk_level": risk_level,
                        "risk_score": final_score,
                        "reasons": list(set(reasons)),
                        "signal": dtl.get("signal"),
                    }
                )

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
# print(json.dumps(networks, indent=4))
