import subprocess
import os
import time
import signal
from PySide6.QtCore import QThread, Signal


class CaptureWorker(QThread):
    # Signal to notify when a handshake is captured, returns the .cap file path
    handshake_found = Signal(str)
    # Signal to notify status updates for the UI log
    status_msg = Signal(str)
    finished = Signal()

    def __init__(self, interface, bssid, chan):
        super().__init__()
        self.interface = interface
        self.bssid = bssid
        self.chan = chan
        self._is_running = True
        self.process = None

    def run(self):
        # Set the storage path in /tmp
        # airodump-ng will automatically append -01.cap to this prefix
        output_prefix = "/tmp/wifi_audit_capture"
        cap_file = f"{output_prefix}-01.cap"

        # Delete old files in /tmp if they exist to avoid confusion
        if os.path.exists(cap_file):
            try:
                # Delete all related files (cap, csv, netxml...)
                subprocess.run(f"sudo rm {output_prefix}-*", shell=True)
            except:
                pass

        self.status_msg.emit(f"[*] Starting capture on channel {self.chan}...")

        # Run airodump-ng in the background
        # Use sudo as these tools require root privileges
        cmd = [
            "sudo",
            "airodump-ng",
            "--bssid",
            self.bssid,
            "-c",
            self.chan,
            "-w",
            output_prefix,
            "--write-interval",
            "1",
            self.interface,
        ]

        try:
            # Launch the process
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                preexec_fn=os.setsid,  # Create a new session to easily kill the entire process group
            )

            # Periodic handshake check loop
            while self._is_running:
                time.sleep(3)  # Check every 3 seconds

                if os.path.exists(cap_file):
                    # Check if the cap file contains a handshake
                    check_cmd = ["aircrack-ng", cap_file]
                    result = subprocess.run(check_cmd, capture_output=True, text=True)

                    if "1 handshake" in result.stdout:
                        self.status_msg.emit("[+] HANDSHAKE CAPTURED!")
                        self.handshake_found.emit(cap_file)
                        break
                    else:
                        self.status_msg.emit("... Waiting for handshake ...")

        except Exception as e:
            self.status_msg.emit(f"[!] Error: {str(e)}")

        finally:
            self.stop_process()
            self.finished.emit()

    def stop_process(self):
        """Safely stop the airodump-ng process"""
        self._is_running = False
        if self.process:
            try:
                # Send SIGINT (Ctrl+C) so airodump closes the cap file correctly
                os.killpg(os.getpgid(self.process.pid), signal.SIGINT)
                self.process.wait(timeout=2)
            except:
                if self.process:
                    self.process.kill()
        self.status_msg.emit("[*] Capture process stopped.")

    def stop(self):
        """External call to stop the thread"""
        self._is_running = False
