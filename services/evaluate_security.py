def evaluate_security(details):
    # Lấy các chuỗi cấu hình để quét keyword
    wpa_info = str(details.get("WPA", "")).upper()
    rsn_info = str(details.get("RSN", "")).upper()
    wps_info = str(details.get("WPS", "")).upper()
    cap_info = str(details.get("capability", "")).upper()

    all_info = f"{wpa_info} {rsn_info} {wps_info} {cap_info}"

    # 1. Kiểm tra WPS (Rủi ro cực cao)
    has_wps = "WPS" in details or "WI-FI PROTECTED SETUP" in all_info
    wps_suffix = " [WPS Enabled - High Vulnerability]" if has_wps else ""

    # 2. Kiểm tra Management Frame Protection (MFP)
    has_mfp = "MFP-CAPABLE" in all_info or "MFP-REQUIRED" in all_info
    mfp_bonus = " (MFP Protected)" if has_mfp else ""

    # 3. Mạng Open hoặc WEP
    # Nếu không có Privacy flag trong capability -> Open
    if "PRIVACY" not in cap_info:
        return "Critical (Open Network - No Encryption)"

    # Nếu có Privacy nhưng không có WPA/RSN block -> Khả năng cao là WEP
    if "WPA" not in details and "RSN" not in details:
        return "Critical (WEP - Legacy/Broken)"

    # 4. Phân tích chuẩn mã hóa mạnh nhất
    # SAE = WPA3
    is_wpa3 = "SAE" in rsn_info

    # RSN = WPA2, WPA = WPA1
    has_rsn = (
        "RSN" in details or "VERSION: 1" in rsn_info
    )  # iw dùng RSN Version 1 cho WPA2
    has_wpa1 = "WPA" in details and "VERSION: 1" in wpa_info

    # 5. Kiểm tra Cipher (TKIP là điểm yếu chết người)
    has_tkip = "TKIP" in all_info
    has_ccmp = "CCMP" in all_info or "AES" in all_info

    # --- PHÂN LOẠI KẾT QUẢ ---

    # Trường hợp WPA3
    if is_wpa3:
        if has_wpa1 or (has_rsn and "PSK" in rsn_info):
            return f"Low-Medium Risk (WPA3 Transition Mode){mfp_bonus}{wps_suffix}"
        return f"Very Low Risk (WPA3-SAE Only){mfp_bonus}{wps_suffix}"

    # Trường hợp Mixed Mode WPA1/WPA2
    if has_rsn and has_wpa1:
        if has_tkip:
            return f"Critical (Mixed WPA1/WPA2 + TKIP){wps_suffix}"
        return f"High Risk (Mixed WPA1/WPA2 AES){wps_suffix}"

    # Trường hợp WPA2 (RSN)
    if has_rsn:
        # Kiểm tra Enterprise
        if "802.1X" in all_info or "IEEE8021X" in all_info or "EAP" in all_info:
            return f"Low Risk (WPA2 Enterprise){mfp_bonus}{wps_suffix}"

        # WPA2-PSK với TKIP
        if has_tkip and not has_ccmp:
            return f"Critical (WPA2 with TKIP Only){wps_suffix}"
        if has_tkip and has_ccmp:
            return f"High Risk (WPA2 TKIP/AES Mixed){wps_suffix}"

        return f"Medium Risk (WPA2-PSK AES){mfp_bonus}{wps_suffix}"

    # Trường hợp WPA1 Legacy
    if has_wpa1:
        return f"High Risk (WPA1 Legacy){wps_suffix}"

    return f"Unknown Security (Manual Check Required: {cap_info}){wps_suffix}"
