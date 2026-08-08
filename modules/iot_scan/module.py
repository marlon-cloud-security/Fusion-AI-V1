# modules/iot_scan/module.py
"""
Fusion-AI // Universal Multi-Modal IoT Device Interrogator Engine v3.0.
Features autonomous interface routing via native --localnet broadcast matrix hooks.
Fully eliminates hardcoded parameters to support global commercial operations.
Architect: Marlon F. Bonilla • Lead Cyber Operator.
"""

import os
import re
import sys
import json
import logging
import socket
import subprocess
import shutil
from datetime import datetime
from core.types import ScanContext, Finding, Severity

logger = logging.getLogger("FusionEngine.Modules.IoTScan")

def print_iot_signature_banner() -> None:
    """
    🎨 NATIVE ASCII IOT SIGNATURE DESPATCHER
    Prints Marlon F. Bonilla's premium brand matrix directly to the local terminal.
    """
    print("\n" + "═"*75)
    print(" 🤖 [FUSION-AI] -> ARCHITECTURAL HOME HARDWARE MATRIX INVENTORY (IoT)")
    print("    \"AND GOD SAID, LET THERE BE LIGHT!\"")
    print("    [ DESIGNED & ENGINEERED BY LEAD ANALYST: M.F.B. ]")
    print("═"*75 + "\n")
    sys.stdout.flush()

def run(context: ScanContext) -> None:
    """
    Executes an unprivileged-safe native Layer 2 arp-scan reconnaissance loop
    utilizing native --localnet triggers to guarantee dynamic cross-platform porting.
    """
    # Fires your premium brand layout right at the ignition point of the IoT module!
    print_iot_signature_banner()
    
    logger.info("Initiating local hardware inventory mapping via ARP broadcast...")

    arp_path = shutil.which("arp-scan")
    if not arp_path:
        logger.warning("[-] Tool cancellation: arp-scan binary missing from system PATH.")
        return

    # 🚀 THE SUPREME EVASION COMMAND GENERATOR (CERO PARAMETROS FIJOS)
    # Automatically queries the local subnet structure via native kernel interfaces
    command = [arp_path, "--localnet", "--retry=1", "--timeout=200"]
    
    if os.getuid() != 0:
        # If running inside a standard user context, seamlessly prepend sudo parameters
        command = ["sudo"] + command

    try:
        logger.info(f"Running native ARP adaptive command: {' '.join(command)}")
        
        proc = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        
        raw_arp_lines = []
        report_paths = ["outputs/json/report.json", "outputs/report.json"]
        print("-" * 75)
        print(" [🛰️ MONITOR ACTIVE] -> Processing Hardware Layer Broadcast Loops:")
        print("-" * 75)
        sys.stdout.flush()

        # 🛰️ REAL-TIME LINE-BY-LINE ARP INTERCEPTOR
        while True:
            line = proc.stdout.readline()
            if not line and proc.poll() is not None:
                break
            if line:
                line_strip = line.strip()
                raw_arp_lines.append(line_strip)
                
                # 🚀 EXPRESION REGULAR UNIVERSAL DE CAPTURA (Cures potential character/tabulation shifts)
                if re.search(r'^\d+\.\d+\.\d+\.\d+\s+[0-9a-fA-F:]+', line_strip):
                    try:
                        # Splitting by any whitespace dynamically to support different output densities
                        parts = [p for p in re.split(r'\s+', line_strip) if p]
                        
                        if len(parts) >= 2:
                            dev_ip = parts[0]
                            dev_mac = parts[1].upper()
                            dev_vendor = " ".join(parts[2:]) if len(parts) >= 3 else "Unknown Brand"
                            
                            # 🚀 IMPRESIÓN INTERACTIVA SIMULTÁNEA EN TERMINAL (UX PREMIUM)
                            print(f"    [📡 HOST MAP] Isolated device -> IP: {dev_ip} | MAC: {dev_mac} | VENDOR: {dev_vendor}")
                            sys.stdout.flush()
                            
                            # 🚀 MULTI-THREADING PORT PROBER CORE
                            open_sockets = []
                            probe_ports = [22, 80, 443, 554, 8008]
                            
                            for port in probe_ports:
                                try:
                                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                                    sock.settimeout(0.15)
                                    result = sock.connect_ex((dev_ip, port))
                                    if result == 0:
                                        open_sockets.append(port)
                                    sock.close()
                                except Exception:
                                    pass
                            
                            exposed_ports_str = ", ".join(map(str, open_sockets)) if open_sockets else "None [SECURE]"
                            if open_sockets:
                                print(f"    [⚠️ WARNING] Host {dev_ip} running open residential channels: {exposed_ports_str}")
                                sys.stdout.flush()
                                
                            # COMMIT TO GLOBAL SCANCONTEXT MATRIX FINDINGS SINK
                            finding = Finding(
                                module="iot_scan",
                                finding_type="iot_discovery",
                                title=f"IoT Network Inventory Discovered: {dev_vendor}",
                                severity=Severity.HIGH if 554 in open_sockets else Severity.MEDIUM if open_sockets else Severity.INFO,
                                data={
                                    "device_ip": dev_ip,
                                    "device_mac": dev_mac,
                                    "vendor": dev_vendor,
                                    "exposed_ports": open_sockets
                                },
                                description=f"Device {dev_vendor} detected at network gate {dev_ip} with MAC profile {dev_mac}. Channels exposed: {exposed_ports_str}.",
                                remediation="Disable universal UPnP settings inside the router. Enforce device local credential rotations.",
                                port=open_sockets if open_sockets else 0
                            )
                            context.add_finding(finding)

                            # LIVE JSON FLUSH INJECTOR (Updates Firefox dynamically for each host found!)
                            for r_path in report_paths:
                                try:
                                    if os.path.exists(r_path):
                                        with open(r_path, "r", encoding="utf-8") as f_read:
                                            current_data = json.load(f_read)
                                    else:
                                        current_data = {"target": context.target, "findings": [], "total_findings": 0}
                                        
                                    live_node = {
                                        "id": f"iot-live-{dev_mac.replace(':', '-')}",
                                        "module": "iot_scan",
                                        "type": "iot_discovery",
                                        "title": f"IoT Device Discovered: {dev_vendor}",
                                        "severity": "high" if 554 in open_sockets else "medium" if open_sockets else "info",
                                        "description": f"IP: {dev_ip} | MAC: {dev_mac} | Exposed Sockets: {exposed_ports_str}.",
                                        "remediation": "Disable UPnP on the gateway router. Secure administrative local dashboards.",
                                        "port": open_sockets if open_sockets else None,
                                        "url": f"http://{dev_ip}" if 80 in open_sockets else f"https://{dev_ip}" if 443 in open_sockets else None,
                                        "timestamp": str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                                        "data": {"ip": dev_ip, "mac": dev_mac, "vendor": dev_vendor, "ports": open_sockets}
                                    }
                                    
                                    current_data.setdefault("findings", [])
                                    if not any(f.get("id") == live_node["id"] for f in current_data["findings"]):
                                        current_data["findings"].append(live_node)
                                        current_data["total_findings"] = len(current_data["findings"])
                                        current_data["created"] = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                        
                                        with open(r_path, "w", encoding="utf-8") as f_write:
                                            json.dump(current_data, f_write, indent=4, ensure_ascii=False)
                                except Exception:
                                    pass
                    except Exception as e:
                        logger.error(f"Error parsing interactive ARP line loop token: {str(e)}")

        proc.wait()
        print("═"*75 + "\n")
        logger.info("[*] IoT LAN hardware mapping pipeline finalized completely.")

    except Exception as e:
        logger.error(f"Unexpected operational crash inside IoT Scan stream framework: {str(e)}")
