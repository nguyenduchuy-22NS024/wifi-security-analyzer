import re
import json
import subprocess


class AnalyzeService:
    def __init__(self, bssid, interface):
        self.bssid = bssid.lower()
        self.interface = interface

    def analyze(self):
        raw_block = self.get_bss_raw_block()
        if not raw_block:
            return {"error": "BSSID not found"}
        parse_data = self._parse_block(raw_block)
        return [parse_data, self.evaluate_quality(parse_data)]

    def get_bss_raw_block(self):
        result = subprocess.run(
            ["sudo", "iw", "dev", self.interface, "scan"],
            capture_output=True,
            text=True,
            check=True,
        )

        raw_data = result.stdout
        bss_blocks = re.split(r"\n(?=BSS\s)", "\n" + raw_data)
        for block in bss_blocks:
            if self.bssid in block.lower():
                return block.strip("\n")
        return None

    def _clean_text(self, text):
        if not text:
            return ""
        text = re.sub(r"^[\s\*]+", "", text)  # Only delete asterisks and spaces
        return text.replace("\t", " ").strip()

    def _parse_block(self, block):
        lines = block.split("\n")
        header = lines[0]
        interface_match = re.search(r"on\s+([^\s\)]+)", header)

        result = {
            "bssid": self.bssid,
            "interface": interface_match.group(1) if interface_match else "unknown",
            "associated": "associated" in header,
            "details": {},
        }

        # Stack saves (indentation, current dictionary)
        stack = [(-1, result["details"])]
        all_lines = [l for l in lines[1:] if l.strip()]

        for i, line in enumerate(all_lines):
            indent = len(line) - len(line.lstrip())
            content = self._clean_text(line)

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
                key = self._clean_text(parts[0])
                val = self._clean_text(parts[1])

                # If you have children or special WPA/RSN/Country entries
                if has_children or key in ["WPA", "RSN", "Country"] or not val:
                    new_node = {}
                    # Handle accompanying content (such as Country: US or WPA: Version 1)
                    if val:
                        if "Environment" in val:  # Only Country
                            env = val.split("Environment:", 1)
                            new_node["Code"] = self._clean_text(env[0])
                            new_node["Environment"] = self._clean_text(env[1])
                        elif ":" in val:
                            sub = val.split(":", 1)
                            new_node[self._clean_text(sub[0])] = self._clean_text(
                                sub[1]
                            )
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

        return result

    #
    def evaluate_quality(self, parsed_data):
        if "error" in parsed_data:
            return None

        details = parsed_data.get("details", {})
        score = 0
        pros = []  # Good points
        cons = []  # Bad points

        # 1. Signal Strength Assessment (Max 40 points)
        signal_str = details.get("signal", "0")
        try:
            signal_val = float(re.search(r"([-+]?\d*\.\d+|\d+)", signal_str).group(1))
            if signal_val >= -55:
                score += 40
                pros.append(f"Excellent signal strength ({signal_val} dBm)")
            elif -70 <= signal_val < -55:
                score += 25
                pros.append(f"Stable signal strength ({signal_val} dBm)")
            else:
                score += 5
                cons.append(f"Weak signal ({signal_val} dBm), prone to instability")
        except:
            cons.append("Could not determine signal strength")

        # 2. Wireless Standard Assessment (Max 30 points)
        if "VHT capabilities" in details:
            score += 25
            pros.append("Supports WiFi 5 (802.11ac) high-speed standard")
        elif "HT capabilities" in details:
            score += 15
            pros.append("Supports WiFi 4 (802.11n) standard")
        else:
            score += 5
            cons.append("Legacy standard (802.11a/b/g) detected, limited speeds")

        if any("HE" in k for k in details.keys()):
            score += 5
            pros.append("Advanced WiFi 6 (HE) technology supported")

        # 3. Frequency Band & Channel Width (Max 20 points)
        freq_str = details.get("freq", "0")
        try:
            freq_val = float(freq_str)
            if freq_val > 4000:  # 5GHz or 6GHz bands
                score += 10
                pros.append("5GHz/6GHz band: High bandwidth and low interference")

                # Check Channel Width
                vht_op = str(details.get("VHT operation", ""))
                if "80 MHz" in vht_op:
                    score += 10
                    pros.append("80MHz channel width: Ultra-fast data transmission")
                elif "40 MHz" in vht_op:
                    score += 5
                    pros.append("40MHz channel width: Decent throughput")
                else:
                    cons.append(
                        "Narrow channel width (20MHz) despite being on high frequency"
                    )
            else:
                score += 5
                cons.append("2.4GHz band: High risk of interference from other devices")
        except:
            pass

        # 4. Security Assessment (Max 10 points)
        if "RSN" in details:
            score += 10
            pros.append("Modern RSN (WPA2/WPA3) security protocol")
        elif "WPA" in details:
            score += 5
            cons.append("Legacy WPA security: Outdated protection")
        else:
            score += 0
            cons.append("No password or WEP: Highly insecure/vulnerable")

        # Classification
        rating = "Poor"
        if score >= 80:
            rating = "Excellent"
        elif score >= 60:
            rating = "Good"
        elif score >= 40:
            rating = "Fair"

        return {
            "total_score": score,
            "rating": rating,
            "analysis": {"pros": pros, "cons": cons},
        }


# service = AnalyzeService("b8:29:03:02:d5:a8", "wlp1s0")
# service = AnalyzeService("cc:71:90:d6:04:49", "wlp1s0")
# print(service.analyze()[0])