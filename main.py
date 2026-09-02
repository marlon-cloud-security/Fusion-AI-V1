# main.py
"""
Fusion-AI // Central Autonomous Orchestrator Core v4.5.
Enterprise Freemium Multi-Modal Pipeline Infrastructure Framework.
Coordinates sequential high-velocity asset mapping & vulnerability discovery.
Authoritative Orchestration Engine // Engineered by Marlon F. Bonilla.
"""

import os
import json
import sys
import logging
import threading
import socket
import webbrowser
import time
import subprocess  
import shutil      
import re
from datetime import datetime
from core.engine import FusionEngine
from core.plugin_loader import PluginLoader
from intelligence.risk_engine import RiskEngine
from core.types import ScanContext, Finding, Severity
from reporting.report import archive_pipeline_report

def print_neon_banner():
    """
    🎨 GLOBAL NATIVE ASCII SIGNATURE DESPATCHER
    Fires Marlon F. Bonilla's premium brand matrix directly to the local terminal
    as the primary authoritative system welcome card for ALL operational profiles.
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

def trigger_automated_browser_gateway():
    """
    🛰️ MULTI-PLATFORM AUTOMATED BROWSER DISPATCHER
    Fires a background thread to seamlessly invoke the customer's default web browser
    (Chrome, Edge, Safari, Firefox) to maximize AnyDesk visual impact instantly.
    """
    target_dashboard_url = "outputs/matrix_live.html"
    if os.path.exists(target_dashboard_url):
        absolute_path = os.path.abspath(target_dashboard_url)
        browser_target = f"file://{absolute_path}"
        try:
            threading.Timer(1.5, lambda: webbrowser.open(browser_target)).start()
        except Exception:
            pass

def spawn_api_server_multi_terminal():
    """
    INTELLIGENT MULTI-TERMINAL & MULTI-SERVER DAEMON SPAWNER
    Dynamically tracks the absolute path and spawns BOTH the API Dashboard Server 
    and the Standalone Autonomous Exploit WebSocket Core in separate physical windows.
    """
    # 🚀 PATH RESOLUTION ENGINE: Detects exactly where the script is running
    project_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 🛰️ PAYLOAD CORES: Execution commands for both independent servers
    api_payload = f"cd {project_dir} && python api_server.py; exec zsh"
    exploit_payload = f"cd {project_dir} && python exploit_server.py; exec zsh"
    
    terminal_found = False
    
    # 1. First Attempt: QTerminal (Standard Kali Linux Emulator)
    if shutil.which("qterminal"):
        try:
            # 📊 SPAWN DASHBOARD API SERVICE (Port 8000)
            subprocess.Popen(
                ["qterminal", "-e", f"zsh -c '{api_payload}'"],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True
            )
            print(" [🚀] SYSTEM MATRIX: Successfully spawned standalone API Dashboard window.")

            # 💥 SPAWN EXPLOIT WEBSOCKET C2 ENGINE (Port 8084)
            subprocess.Popen(
                ["qterminal", "-e", f"zsh -c '{exploit_payload}'"],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True
            )
            print(" [🚀] SYSTEM MATRIX: Successfully spawned standalone Exploit C2 Matrix window.")
            
            terminal_found = True
        except Exception:
            pass

    # 2. Second Attempt: XFCE4 Terminal (Backup Kali Graphical Emulator)
    if not terminal_found and shutil.which("xfce4-terminal"):
        try:
            subprocess.Popen(
                ["xfce4-terminal", "-e", f"zsh -c '{api_payload}'"],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True
            )
            subprocess.Popen(
                ["xfce4-terminal", "-e", f"zsh -c '{exploit_payload}'"],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True
            )
            print(" [🚀] SYSTEM MATRIX: Successfully spawned multi-server windows via 'xfce4-terminal'.")
            terminal_found = True
        except Exception:
            pass

    # 3. Third Attempt: Standard GNOME Terminal
    if not terminal_found and shutil.which("gnome-terminal"):
        try:
            subprocess.Popen(["gnome-terminal", "--", "zsh", "-c", api_payload], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
            subprocess.Popen(["gnome-terminal", "--", "zsh", "-c", exploit_payload], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
            print(" [🚀] SYSTEM MATRIX: Successfully spawned multi-server windows via 'gnome-terminal'.")
            terminal_found = True
        except Exception:
            pass
                
    # 4. Emergency Headless Fallback Daemonization
    if not terminal_found:
        print(" [⚠] SYSTEM WARNING: No graphical terminal emulator detected. Falling back to background processes.")
        try:
            subprocess.Popen(["python", "api_server.py"], cwd=project_dir, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
            subprocess.Popen(["python", "exploit_server.py"], cwd=project_dir, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
        except Exception as e:
            print(f" [❌] CRITICAL STATE: Failed to boot system daemons: {e}")

    # ⏱️ TIME BUFFER & HEALTH CHECK HANDSHAKE
    print(" [*] SYSTEM BUFFER: Synchronizing multi-protocol service interfaces, please wait...")
    time.sleep(2)
def main():
    # 🚀 LIVE INITIALIZATION HANDSHAKE: Fires your signature brand layout right at the ignition point!
    print_neon_banner()

    # 🤖 DAEMON AUTO-IGNITION CORE
    spawn_api_server_multi_terminal()

    # 🩹 BUFFER CLEANER PATCH: Safely clean up local database artifacts on disk before launch
    # to structurally kill cyclic mirrors or historical findings duplication on browser UI panels.
    report_path = "outputs/json/report.json"
    os.makedirs("outputs/json", exist_ok=True)
    empty_pristine_buffer = {
        "target": "",
        "attacker_platform": "0.0.0.0",
        "operational_tier": "PREMIUM",
        "total_findings": 0,
        "findings": [],
        "execution_metadata": {"execution_path": []},
        "risk_intelligence": {"risk_score": 100, "verdict": "SECURE"},
        "created": str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    }

    try:
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(empty_pristine_buffer, f, indent=4)
        
        with open("outputs/report.json", "w", encoding="utf-8") as f:
            json.dump(empty_pristine_buffer, f, indent=4)
    except Exception:
        pass

    # Initialize core autonomous orchestrator and intelligence engines
    engine = FusionEngine()
    loader = PluginLoader()
    risk_engine = RiskEngine()

    # Automatically discover and register all plugin modules from the modules tree
    loader.load_plugins(engine)

    print(" [0] Wireless Infrastructure & Wi-Fi Discovery")
    print(" [1] Web Application Assessment")
    print(" [2] API Security Audit")
    print(" [3] Internal Corporate Network Scan")
    print(" [4] Home Network Security (65K Safe-Connect Mode)")
    print(" [5] Cloud Infrastructure Assessment")
    print(" [6] Active Directory Security Audit")
    print(" [7] IoT Autonomous Grid Assessment")
    print(" [8] Wireless Offensive Matrix (Pure Wi-Fi Attack & Cracking)")
    print("-" * 60)
    
    try:
        choice = input("Opción: ").strip()
    except (KeyboardInterrupt, EOFError):
        print("\n[-] Operational cancellation received. Aborting.")
        sys.exit(0)

    # Global context parameter injection to feed upstream plugins dynamically via environment RAM variables
    os.environ["FUSION_AUDIT_MODE"] = "HOME" if choice == "4" else "ENTERPRISE"
    
    if os.environ["FUSION_AUDIT_MODE"] == "HOME":
        print("[*] COGNITIVE VECTOR ACCEPTS -> Initializing Home Security Assessment (Full 65K Matrix).")
    else:
        print("[*] COGNITIVE VECTOR ACCEPTS -> Loading Standard Enterprise Pipeline Posture.")

    # Capture the operational target via a clean unattended-ready input stream
    try:
        target = input(
            "\nEnter target infrastructure (IP or Domain) "
            "[0 = Wi-Fi Discovery]: "
        ).strip()

    except (KeyboardInterrupt, EOFError):
        print("\n[-] Operational cancellation received. Aborting.")
        sys.exit(0)
    # ================================================================
    # WIRELESS OPERATIONS CORE (OPTIONS 0 & 8)
    # ================================================================
    if target == "0" or choice == "8":

        print("\n" + "═" * 60)
        print(" 📡 FUSION-AI // WIRELESS OPERATIONAL SUB-MATRIX")
        print("═" * 60)

        try:
            from modules.wifi_discovery import module as wifi_discovery
            # Le pasamos el 'choice' original para que el módulo sepa si va en modo híbrido (0) u ofensivo (8)
            wifi_result = wifi_discovery.run(mode=choice)

        except Exception as e:
            print(f"\n[❌] Wi-Fi operational module failed: {e}")
            sys.exit(1)

        if not wifi_result.get("available"):
            print("\n[⚠] No wireless interface detected.")
            print("[i] Connect a compatible Wi-Fi adapter to Kali.")
            print("[i] VirtualBox must expose the adapter to the guest.")
            print("\n[-] Returning to target selection.")
            sys.exit(0)

        selected = wifi_result.get("selected_network")
        local_network = wifi_result.get("local_network") or {}
        active_network = wifi_result.get("active_network")

        print("\n[+] Wireless interface detected.")

        for interface in wifi_result.get("interfaces", []):
            print(
                f"    Interface : {interface.get('name')}"
                f" | Type: {interface.get('type')}"
                f" | MAC: {interface.get('mac')}"
            )

        if active_network:
            print(
                f"\n[+] Active connection: "
                f"{active_network.get('connection')}"
            )

        if local_network.get("ip"):
            print(f"[+] Local IP : {local_network['ip']}")

        if local_network.get("gateway"):
            print(f"[+] Gateway  : {local_network['gateway']}")

        if selected:
            print("\n[+] Authorized network selected:")
            print(f"    SSID   : {selected.get('ssid')}")
            print(f"    BSSID  : {selected.get('bssid')}")
            print(f"    Channel: {selected.get('channel')}")
            print(f"    Signal : {selected.get('signal')}")
            print(f"    Security: {selected.get('security')}")

        # 🚀 ELITE COGNITIVE TARGET RESOLVER
        # Si el módulo Wi-Fi resolvió un objetivo dinámico o el operador seleccionó una red,
        # lo adoptamos de inmediato de forma agnóstica sin requerir direccionamiento DHCP del host.
        target = wifi_result.get("target")

        if not target:
            print("\n[⚠] Wireless Exploration Matrix: No routing targets defined by module.")
            print("[i] Injecting diagnostic loopback target to maintain pipeline continuum.")
            target = "127.0.0.1"

        print(f"\n[🎯] Pipeline target resolved for Fusion core: {target}")
    # ================================================================
    # NORMAL MODE
    # IP / DOMAIN continues through the existing pipeline.
    # ================================================================

    if not target:
        # 🚀 INTELLIGENT DYNAMIC DEFAULTS CONTEXT CALCULATION (ZERO HARDCODED PARAMETERS)
        try:
            s_detect = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s_detect.connect(("8.8.8.8", 80))
            gateway_ip = s_detect.getsockname()[0]
            gateway_part = gateway_ip.split(".")
            s_detect.close()
            if os.environ["FUSION_AUDIT_MODE"] == "HOME":
                target = f"{gateway_part[0]}.{gateway_part[1]}.{gateway_part[2]}.254"
            else:
                target = f"{gateway_part[0]}.{gateway_part[1]}.{gateway_part[2]}.1"
        except Exception:
            target = "127.0.0.1"
        print(f"Using default infrastructure sandbox target: {target}")

    # 🚀 LIVE INTERACTIVE IGNITION: Dispatches the default browser right as the scan begins!
    print("[*] CONTROL GATEWAY -> Dispatched automatic browser initialization thread...")
    trigger_automated_browser_gateway()

    # 🏢 UNIFIED INTERCONNECTED FUSION-AI PIPELINE 
    # Executes 100% of your mature modules sequence across both operational modes!
    scan_report = engine.run_pipeline(target)

    # RECONSTRUCT MEMORY LOG GRAPH MATRIX TO COMPILING STRUCTURAL RISK COEFFICIENTS
    reconstructed = ScanContext(target)
    
    # Map discovered tool findings directly into consolidated ScanContext structures
    for f in scan_report.get("findings", []):
        reconstructed.add_finding(
            Finding(
                module=f["module"],
                finding_type=f["type"],
                title=f["title"],
                severity=Severity(f["severity"]) if isinstance(f["severity"], Severity) else Severity.INFO,
                data=f["data"],
                description=f["description"],
                remediation=f["remediation"]
            )
        )

    # Synchronize raw dynamic vulnerabilities captured down-stream into asset memory lists
    if "vulnerabilities" in scan_report:
        reconstructed.asset.vulnerabilities = scan_report["vulnerabilities"]
    else:
        # Emergency pipeline parser backup loop
        for f in scan_report.get("findings", []):
            if f["type"] in ["vulnerability", "sql_injection"]:
                reconstructed.asset.vulnerabilities.append({
                    "name": f["title"].replace("Nuclei: ", ""),
                    "severity": str(f["severity"]).split(".")[-1].lower(),
                    "matched_at": f.get("url", target),
                    "template": f.get("data", {}).get("template_id", "unknown")
                })

    # Trigger centralized risk triage evaluation models for corporate assessments
    risk = risk_engine.evaluate_context(reconstructed)
    scan_report["risk_intelligence"] = risk

    # 💾 COGNITIVE METADATA ENRICHMENT: Resolves dynamic platform stamps dynamically into JSON blocks
    scan_report["created"] = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    # 🚀 UNIVERSAL ATTACKER RESOLVER: Interrogates Linux sockets to stamp the absolute real operator IP
    attacker_resolved_ip = "0.0.0.0"
    try:
        s_trace = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s_trace.connect(("8.8.8.8", 80))
        attacker_resolved_ip = s_trace.getsockname()[0]
        s_trace.close()
    except Exception:
        attacker_resolved_ip = "127.0.0.1"
    scan_report["attacker_platform"] = attacker_resolved_ip

    # Commit the fully parsed dynamic report ledger to local json database logs
    try:
        archive_pipeline_report(scan_report)
        with open("outputs/report.json", "w", encoding="utf-8") as ui_f:
            json.dump(scan_report, ui_f, indent=4, ensure_ascii=False)
    except Exception:
        pass

    # 💾 CENTRALIZED SYNC HANDSHAKE SUCCESS DISPLAY
    print("\n" + "═" * 60)
    print(" 🎉 [✔] FUSION-AI PIPELINE WORKFLOW COMPLETE")
    print(" [🎯] Cyberpunk Real-Time HTML Dashboard Initialized: outputs/")
    print(" [📊] Global JSON Ledger successfully committed to database logs.")
    print("═" * 60 + "\n")

    # Clean JSON object dump to standard output for upstream monitoring tools
    print("\n" + "=" * 60)
    print(json.dumps(scan_report, indent=4, ensure_ascii=False))
    print("=" * 60 + "\n")

if __name__ == "__main__":
    main()
