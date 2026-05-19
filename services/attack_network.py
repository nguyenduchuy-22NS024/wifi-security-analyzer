import subprocess
import re

def toggle_monitor_mode(interface):
    """
    Bật hoặc tắt Monitor Mode. 
    Trả về (success: bool, new_interface_name: str, message: str)
    """
    try:
        # 1. Kiểm tra trạng thái hiện tại của interface bằng lệnh 'iw dev'
        status_check = subprocess.run(["iw", "dev", interface, "info"], capture_output=True, text=True)
        
        # Nếu interface đang ở chế độ 'managed', chúng ta sẽ BẬT monitor
        if "type managed" in status_check.stdout:
            # Bước phụ: Dọn dẹp các tiến trình gây nhiễu (NetworkManager, wpa_supplicant)
            # Lưu ý: Lệnh này có thể làm mất kết nối internet tạm thời
            subprocess.run(["sudo", "airmon-ng", "check", "kill"], stdout=subprocess.DEVNULL)
            
            # Chạy lệnh start
            result = subprocess.run(["sudo", "airmon-ng", "start", interface], capture_output=True, text=True)
            
            if result.returncode == 0:
                # Tìm tên interface mới (thường thêm 'mon' ở cuối)
                # Ví dụ: wlan0 -> wlan0mon
                new_name = interface + "mon" 
                # Cách an toàn hơn: quét lại tên interface thực tế trong output
                match = re.search(r"monitor mode enabled on (\w+)", result.stdout)
                if match:
                    new_name = match.group(1)
                    
                return True, new_name, f"Monitor Mode ON: {new_name}"
            
        # Nếu interface đang ở chế độ 'monitor', chúng ta sẽ TẮT monitor
        elif "type monitor" in status_check.stdout:
            result = subprocess.run(["sudo", "airmon-ng", "stop", interface], capture_output=True, text=True)
            
            if result.returncode == 0:
                # Tìm tên interface cũ sau khi stop (thường bỏ 'mon')
                new_name = interface.replace("mon", "")
                match = re.search(r"monitor mode disabled on (\w+)", result.stdout)
                if match:
                    new_name = match.group(1)
                
                # Sau khi tắt monitor, nên khởi động lại NetworkManager để có lại mạng
                subprocess.run(["sudo", "systemctl", "start", "NetworkManager"], stdout=subprocess.DEVNULL)
                
                return True, new_name, f"Monitor Mode OFF: {new_name}"
        
        return False, interface, "Error interface."

    except Exception as e:
        return False, interface, f"Error system: {str(e)}"