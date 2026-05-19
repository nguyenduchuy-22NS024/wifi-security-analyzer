import subprocess
import os
import re
from PySide6.QtCore import QThread, Signal


class CrackWorker(QThread):
    status_msg = Signal(str)
    result_found = Signal(bool, str)
    finished = Signal()

    def __init__(self, cap_file, wordlist_path, bssid):
        super().__init__()
        self.cap_file = cap_file
        self.wordlist_path = wordlist_path
        self.bssid = bssid
        self._is_running = True
        self.process = None
        # Regex để tìm và loại bỏ ANSI escape codes
        self.ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")

    def clean_ansi(self, text):
        """Loại bỏ các mã định dạng Terminal (ANSI codes)"""
        return self.ansi_escape.sub("", text)

    def run(self):
        if not os.path.exists(self.cap_file):
            self.result_found.emit(False, "Capture file (.cap) not found")
            return
        if not os.path.exists(self.wordlist_path):
            self.result_found.emit(False, "Wordlist file not found")
            return

        self.status_msg.emit("[*] Starting the cracking process...")
        self.status_msg.emit(f"[*] Target: {self.bssid}")
        self.status_msg.emit(f"[*] Wordlist: {os.path.basename(self.wordlist_path)}")

        # Chạy lệnh với tùy chọn không màu nếu có thể, nhưng regex vẫn an toàn nhất
        cmd = [
            "aircrack-ng",
            "-a",
            "2",
            "-b",
            self.bssid,
            "-w",
            self.wordlist_path,
            self.cap_file,
        ]

        try:
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True,
            )

            found_password = None

            for raw_line in self.process.stdout:
                if not self._is_running:
                    break

                # Làm sạch dòng dữ liệu khỏi mã ANSI
                line = self.clean_ansi(raw_line).strip()
                if not line:
                    continue

                # Hiển thị tiến trình lên UI (loại bỏ các dòng rác)
                if "keys tested" in line.lower():
                    self.status_msg.emit(line)

                # Kiểm tra kết quả bẻ khóa
                if "KEY FOUND!" in line:
                    # Logic tách chuỗi mới: Tìm phần nằm trong dấu [ ] cuối cùng của dòng
                    # Ví dụ dòng sạch: "KEY FOUND! [ p419ktx2 ]"
                    matches = re.findall(r"\[\s*(.*?)\s*\]", line)
                    if matches:
                        found_password = matches[
                            -1
                        ]  # Lấy kết quả ở dấu ngoặc cuối cùng
                        break

            self.process.wait()

            if found_password:
                # Xóa sạch các ký tự điều khiển còn sót lại nếu có
                found_password = "".join(c for c in found_password if c.isprintable())
                self.status_msg.emit(f"\n[!!!] SUCCESS! Password is: {found_password}")
                self.result_found.emit(True, found_password)
            elif not self._is_running:
                self.status_msg.emit("\n[!] Cracking stopped by user.")
            else:
                self.status_msg.emit("\n[!] Failed: Password not found in wordlist.")
                self.result_found.emit(False, "Password not found.")

        except Exception as e:
            self.status_msg.emit(f"[!] System error: {str(e)}")
            self.result_found.emit(False, str(e))

        finally:
            self.stop_process()
            self.finished.emit()

    def stop_process(self):
        self._is_running = False
        if self.process:
            try:
                self.process.terminate()
                self.process.kill()
            except:
                pass

    def stop(self):
        self._is_running = False
        if self.process:
            try:
                self.process.terminate()
                self.process.kill()
            except:
                pass
