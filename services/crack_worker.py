import subprocess
import os
import signal
from PySide6.QtCore import QThread, Signal


class CrackWorker(QThread):
    # Send status logs to the UI
    status_msg = Signal(str)
    # Send final result (Success boolean, Password or error message)
    result_found = Signal(bool, str)
    finished = Signal()

    def __init__(self, cap_file, wordlist_path, bssid):
        super().__init__()
        self.cap_file = cap_file
        self.wordlist_path = wordlist_path
        self.bssid = bssid
        self._is_running = True
        self.process = None

    def run(self):
        # Check if files exist
        if not os.path.exists(self.cap_file):
            self.result_found.emit(False, "Capture file (.cap) not found")
            return
        if not os.path.exists(self.wordlist_path):
            self.result_found.emit(False, "Wordlist file not found")
            return

        self.status_msg.emit("[*] Starting the cracking process...")
        self.status_msg.emit(f"[*] Target: {self.bssid}")
        self.status_msg.emit(f"[*] Wordlist: {os.path.basename(self.wordlist_path)}")

        # aircrack-ng command
        # -w: path to wordlist
        # -b: Target BSSID
        cmd = ["aircrack-ng", "-w", self.wordlist_path, "-b", self.bssid, self.cap_file]

        try:
            # Run the process and read real-time output
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True,
            )

            found_password = None

            # Read each line of output to find the result
            for line in self.process.stdout:
                if not self._is_running:
                    break

                # Log progress (e.g., "1000 keys tested (500.23 k/s)")
                if "tested" in line.lower():
                    self.status_msg.emit(line.strip())

                # Check if the key was found
                if "KEY FOUND!" in line:
                    # Extract the password from: [ KEY FOUND! [ password ] ]
                    start = line.find("[") + 1
                    end = line.find("]", start)
                    # Extract string within the second set of brackets
                    start_pass = line.find("[", end) + 1
                    end_pass = line.find("]", start_pass)
                    found_password = line[start_pass:end_pass].strip()
                    break

            self.process.wait()

            if found_password:
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
        """Stop the cracking process"""
        self._is_running = False
        if self.process:
            try:
                self.process.terminate()
                self.process.kill()
            except:
                pass

    def stop(self):
        """Public method to stop the thread from UI"""
        self._is_running = False
