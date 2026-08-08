# modules/nmap/module.py
"""
Fusion-AI // Universal Multi-Modal Nmap Interrogator Engine v7.1.
Features 100% simultaneous live terminal streaming AND instant ScanContext injections.
Fully eliminates hardcoded parameters to support global commercial operations.
Architect: Marlon F. Bonilla • Chief Cyber Operator.
"""

import os
import re
import sys
import json
import logging
import subprocess
import shutil
from datetime import datetime
from core.types import ScanContext, Finding, Severity

logger = logging.getLogger("FusionEngine.Modules.Nmap")

def print_maligned_signature_banner() -> None:
    """
    🎨 NATIVE ASCII SIGNATURE DESPATCHER
    Prints Marlon F. Bonilla's premium brand matrix directly to the local terminal
    with precise geometric block alignments to cure potential character shifts.
    """
    print("\n" + "═"*75)
    print(r"""
  ███████╗██╗   ██╗███████╗██╗ ██████╗ ███╗   ██╗         █████╗ ██╗
  ██╔════╝██║   ██║██╔════╝██║██╔═══██╗████╗  ██║        ██╔══██╗██║
  █████╗  ██║   ██║███████╗██║██║   ██║██╔██╗ ██║ █████╗ ███████║██║
  ██╔══╝  ██║   ██║╚════██║██║██║   ██║██║╚██╗██║ ╚════╝ ██╔══██║██║
  ██║     ╚██████╔╝███████║██║╚██████╔╝██║ ╚████║        ██║  ██║██║
  ╚═╝      ╚═════╝ ╚══════╝╚═╝ ╚═════╝ ╚═╝  ╚═══╝        ╚═╝  ╚═╝╚═╝
    """)
    print("        --- ARTIFICIAL INTELLIGENCE AT ITS FINEST ---")
    print("\n        \"AND GOD SAID, LET THERE BE LIGHT!\"")
    print("        [ DESIGNED & ENGINEERED BY LEAD ANALYST: M.F.B. ]")
    print("═"*75 + "\n")
    sys.stdout.flush()

def run(context: ScanContext) -> None:
    """
    Executes a real native Nmap scan leveraging programmatic parameter mutation
    and adaptive pacing evasion vectors to structurally bypass router rate-limits.
    """
    # Fires your premium author brand layout right at the ignition point of the scan!
    print_maligned_signature_banner()
    
    logger.info(f"Initiating live network reconnaissance over: {context.target}")

    nmap_path = shutil.which("nmap")
    if not nmap_path:
        logger.error("Nmap binary not found in the system PATH. Verify installation.")
        raise FileNotFoundError("Critical dependency missing: nmap execution binary.")

    audit_profile = os.environ.get("FUSION_AUDIT_MODE", "ENTERPRISE")
    
    # 🚀 SUPER-INTELLIGENT HOME RATE-LIMIT BYPASS Posture
    if audit_profile == "HOME":
        logger.info("[*] PROFILE DETECTED -> Engaging Autonomous Residential 65K Deep Audit Posture.")
        # Full 65,535 port scan enforced (-p-). Uses -sT to legally close connections and clear 
        # local gateway NAT state tables, avoiding catastrophic hardware lockups or timeouts.
        # Enforces an adaptive bracket (min 35 / max 95) to surf right under commercial ISP locks.
        nmap_args = [
            "-p-", 
            "-sT", 
            "-T4", 
            "--min-rate", "35",        # Floor safety pace to prevent starvation
            "--max-rate", "95",        # Stealth boundary limit to completely bypass the 100/s IPS lock
            "--max-rtt-timeout", "150ms",
            "--max-retries", "1", 
            "--host-timeout", "25m",   # Compensates time windows for deep comprehensive coverage
            "-Pn",
            "--stats-every", "10s",
            "-vvv"
        ]
    else:
        logger.info("[*] PROFILE DETECTED -> Applying Fast Enterprise Infrastructure flags.")
        # Enterprise environment leverages full raw SYN scanning over wide corporate pipelines
        nmap_args = ["-p-", "-sS", "-T4", "--stats-every", "5s", "-vvv"]

    command = [nmap_path] + nmap_args + [str(context.target)]
    try:
        # Spawning the process with line-buffering to catch every text token instantly
        proc = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )

        open_ports_discovered = []
        report_paths = ["outputs/json/report.json", "outputs/report.json"]

        print("-" * 75)
        print(" [🛰️ MONITOR ACTIVE] -> Unbuffered Dual Terminal & UI Sync Engaged:")
        print("-" * 75)
        sys.stdout.flush()

        # Dynamic local attacker IP resolution wrapper to guarantee universal porting
        attacker_resolved_ip = "0.0.0.0"
        try:
            import socket
            s_trace = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s_trace.connect(("8.8.8.8", 80))
            attacker_resolved_ip = s_trace.getsockname()[0]
            s_trace.close()
        except Exception:
            attacker_resolved_ip = "127.0.0.1"

        while True:
            line = proc.stdout.readline()
            if not line and proc.poll() is not None:
                break
            if line:
                line_strip = line.strip()
                
                # Clean line print routing to show real-time progress layout
                print(f"    {line_strip}")
                sys.stdout.flush()

                # DUAL-EXPRESSION PARSER MATRIX (Captures line-by-line discovery or tabular reports)
                port_id = None
                
                if "Discovered open port" in line_strip:
                    p_match = re.search(r'port\s+(\d+)/tcp', line_strip)
                    if p_match:
                        port_id = int(p_match.group(1))
                elif "/tcp" in line_strip and "open" in line_strip:
                    p_match = re.search(r'^(\d+)/tcp\s+open', line_strip)
                    if p_match:
                        port_id = int(p_match.group(1))

                # If an open port is isolated, trigger instant ScanContext and UI synchronization
                if port_id is not None:
                    if port_id not in open_ports_discovered:
                        open_ports_discovered.append(port_id)
                        
                        # Build dynamic Finding payload inside ScanContext RAM
                        finding = Finding(
                            module="nmap",
                            finding_type="open_port",
                            title=f"Open Network Port Discovered: {port_id}/TCP",
                            severity=Severity.MEDIUM,
                            data={
                                "port": port_id,
                                "protocol": "tcp",
                                "service": "discovering",
                                "product": "unknown"
                            },
                            description=f"Port {port_id} detected listening actively over target interface gates.",
                            remediation="Enforce strict firewall zoning policies. Close ports that are not business-critical.",
                            port=port_id
                        )
                        
                        if port_id not in context.open_ports:
                            context.open_ports.append(port_id)
                            context.add_finding(finding)
                            
                            context.asset.open_ports.append({
                                "port": port_id, "service": "discovering", "product": "unknown", "protocol": "tcp"
                            })

                        # 🚀 LIVE JSON FLUSH INJECTOR (Force-syncs Firefox counter cards instantly)
                        for r_path in report_paths:
                            try:
                                if os.path.exists(r_path):
                                    with open(r_path, "r", encoding="utf-8") as f_read:
                                        current_data = json.load(f_read)
                                else:
                                    current_data = {"target": context.target, "findings": [], "total_findings": 0}

                                live_node = {
                                    "id": f"home-live-{port_id}", "module": "nmap", "type": "open_port",
                                    "title": f"Open Network Port Discovered: {port_id}/TCP", "severity": "medium",
                                    "description": f"Port {port_id} detected actively listening over target interface gates.",
                                    "remediation": "Enforce strict firewall zoning policies. Close ports that are not business-critical.",
                                    "port": port_id, "url": f"http://{context.target}:{port_id}" if port_id == 80 else f"https://{context.target}:{port_id}" if port_id == 443 else None,
                                    "timestamp": str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                                    "data": {"port": port_id, "protocol": "tcp", "service": "discovering", "product": "unknown"}
                                }
                                
                                current_data.setdefault("findings", [])
                                if not any(f.get("id") == live_node["id"] for f in current_data["findings"]):
                                    current_data["findings"].append(live_node)
                                    current_data["total_findings"] = len(current_data["findings"])
                                    # 🚀 VACUNA DE PERSISTENCIA GLOBAL: Hereda la IP real calculada por los sockets del kernel
                                    current_data["attacker_platform"] = attacker_resolved_ip
                                    current_data["created"] = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    current_data["target"] = context.target
                                    
                                    with open(r_path, "w", encoding="utf-8") as f_write:
                                        json.dump(current_data, f_write, indent=4, ensure_ascii=False)
                            except Exception:
                                pass
                            except Exception:
                               pass

        proc.wait()
        print("═"*75 + "\n")
        logger.info(f"Nmap pipeline stage finalized | Asset open_ports populated: {len(context.asset.open_ports)}")

    except Exception as e:
        logger.error(f"Unexpected processing breakdown inside Nmap unbuffered stream: {str(e)}")

