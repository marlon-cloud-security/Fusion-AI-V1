# modules/iot_scan/module.py
"""
Fusion-AI // Universal Multi-Modal IoT Device Interrogator Engine v4.0 - PREMIUM
Features autonomous interface routing via native --localnet broadcast matrix hooks.
Fully eliminates hardcoded parameters to support global commercial operations.
Architect: Marlon F. Bonilla • Lead Cyber Operator.
Developed in collaboration with Success Team AI Dynamics.
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
    utilizing the identical linear architecture of Gobuster to eliminate duplication.
    """
    print_iot_signature_banner()
    logger.info("Initiating local hardware inventory mapping via ARP broadcast...")

    arp_path = shutil.which("arp-scan")
    if not arp_path:
        logger.warning("[-] Tool cancellation: arp-scan binary missing from system PATH.")
        return

    command = [arp_path, "--localnet", "--retry=1", "--timeout=200"]
    if os.getuid() != 0:
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
        
        print("-" * 75)
        print(" [🛰️ MONITOR ACTIVE] -> Processing Hardware Layer Broadcast Loops:")
        print("-" * 75)
        sys.stdout.flush()
        # 🛰️ BUCLE LINEAL DE INTERCEPCIÓN ARP DIRECTA (ESTILO GOBUSTER)
        while True:
            line = proc.stdout.readline()
            if not line and proc.poll() is not None:
                break
            if line:
                line_strip = line.strip()
                
                # Expresión regular universal para aislar la IP y la MAC en caliente
                if re.search(r'^\d+\.\d+\.\d+\.\d+\s+[0-9a-fA-F:]+', line_strip):
                    try:
                        parts = [p for p in re.split(r'\s+', line_strip) if p]
                        if len(parts) >= 2:
                            dev_ip = parts[0]
                            dev_mac = parts[1].upper()
                            dev_vendor = " ".join(parts[2:]) if len(parts) >= 3 else "Unknown Brand"
                            
                            print(f"    [📡 HOST MAP] Isolated device -> IP: {dev_ip} | MAC: {dev_mac} | VENDOR: {dev_vendor}")
                            sys.stdout.flush()
                            
                            # Mapeo rápido de puertos residenciales estándar
                            open_sockets = []
                            probe_ports = [22, 80, 443, 554, 8008]
                            for port in probe_ports:
                                try:
                                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                                    sock.settimeout(0.1)
                                    if sock.connect_ex((dev_ip, port)) == 0:
                                        open_sockets.append(port)
                                    sock.close()
                                except Exception:
                                    pass
                            
                            exposed_str = ", ".join(map(str, open_sockets)) if open_sockets else "None [SECURE]"
                            
                            # 🚀 INYECCIÓN DIRECTA SÍNCRONA ÚNICA AL CONTEXTO CORE (MÉTODO GOBUSTER CORREGIDO)
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
                                description=f"Device {dev_vendor} detected at network gate {dev_ip} with MAC profile {dev_mac}. Channels exposed: {exposed_str}.",
                                remediation="Disable universal UPnP settings inside the router. Enforce device local credential rotations.",
                                port=open_sockets if open_sockets else 0
                            )
                            context.add_finding(finding)
                            
                    except Exception as e:
                        logger.error(f"Error parsing interactive ARP line loop token: {str(e)}")

        proc.wait()
        print("═"*75 + "\n")
        logger.info("[*] IoT LAN hardware mapping pipeline finalized completely.")

    except Exception as e:
        logger.error(f"Unexpected operational crash inside IoT Scan stream framework: {str(e)}")
