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
import platform
from datetime import datetime
from core.engine import FusionEngine
from core.plugin_loader import PluginLoader
from intelligence.risk_engine import RiskEngine
from core.types import ScanContext, Finding, Severity
from reporting.report import archive_pipeline_report
# 📡 CONECTIVIDAD DE LA SUITE OFENSIVA INALÁMBRICA (OPCIÓN 9)
from modules.wireless_suite import module as wireless_suite

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
    project_dir = os.path.dirname(os.path.abspath(__file__))
    api_payload = f"cd {project_dir} && python api_server.py; exec zsh"
    exploit_payload = f"cd {project_dir} && python exploit_server.py; exec zsh"
    
    terminal_found = False
    
    if shutil.which("qterminal"):
        try:
            subprocess.Popen(
                ["qterminal", "-e", f"zsh -c '{api_payload}'"],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True
            )
            print(" [🚀] SYSTEM MATRIX: Successfully spawned standalone API Dashboard window.")
            subprocess.Popen(
                ["qterminal", "-e", f"zsh -c '{exploit_payload}'"],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True
            )
            print(" [🚀] SYSTEM MATRIX: Successfully spawned standalone Exploit C2 Matrix window.")
            terminal_found = True
        except Exception:
            pass

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

    if not terminal_found and shutil.which("gnome-terminal"):
        try:
            subprocess.Popen(["gnome-terminal", "--", "zsh", "-c", api_payload], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
            subprocess.Popen(["gnome-terminal", "--", "zsh", "-c", exploit_payload], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
            print(" [🚀] SYSTEM MATRIX: Successfully spawned multi-server windows via 'gnome-terminal'.")
            terminal_found = True
        except Exception:
            pass
                
    if not terminal_found:
        print(" [⚠] SYSTEM WARNING: No graphical terminal emulator detected. Falling back to background processes.")
        try:
            subprocess.Popen(["python", "api_server.py"], cwd=project_dir, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
            subprocess.Popen(["python", "exploit_server.py"], cwd=project_dir, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
        except Exception as e:
            print(f" [❌] CRITICAL STATE: Failed to boot system daemons: {e}")

    print(" [*] SYSTEM BUFFER: Synchronizing multi-protocol service interfaces, please wait...")
    time.sleep(2)
def main():
    print_neon_banner()
    spawn_api_server_multi_terminal()

    # 📡 INITIALIZING INTERACTIVE KALI GLOBAL TERMINAL SYSTEM (SaaS Architecture)
    import api_server
    import pty  # Importación del módulo nativo de control de terminales físicas
    log_dir = "outputs/logs"
    os.makedirs(log_dir, exist_ok=True)
    global_log = os.path.join(log_dir, "fusion_bettercap_stream.log")
    
    try:
        # Open master and slave pseudo-terminal descriptors
        master_fd, slave_fd = pty.openpty()
        
        shell_process = subprocess.Popen(
            ["zsh", "-i"],
            stdin=master_fd,
            stdout=open(global_log, "wb"),
            stderr=subprocess.STDOUT,
            bufsize=0,
            start_new_session=True
        )
        
        shell_process.master_fd = master_fd
        api_server.GLOBAL_SESSIONS["bettercap_session"] = shell_process
        
        # Enforce global asynchronous monitoring flags
        os.environ["FUSION_SUBPROCESS_ACTIVE"] = "TRUE"
        
        # Instantiate and spin up the live chronological background monitoring thread
        reconstructed_context = ScanContext(target if 'target' in locals() else "127.0.0.1")
        monitor_thread = threading.Thread(
            target=monitor_live_logs,
            args=(global_log, "Interactive Shell", "manual_terminal_session", reconstructed_context),
            daemon=True
        )
        monitor_thread.start()
        
        print(" [🚀] SYSTEM MATRIX: Successfully established global persistent Kali Shell session.")
        os.write(master_fd, b"\n")
    except Exception as shell_exc:
        print(f" [⚠] SYSTEM WARNING: Core failed to spin up interactive shell daemon: {shell_exc}")

    # 🩹 BUFFER CLEANER PATCH: Safely clean up local database artifacts on disk before launch
    report_path = "outputs/json/report.json"
    os.makedirs("outputs/json", exist_ok=True)
    empty_pristine_buffer = {
        "target": "",
        "attacker_platform": "0.0.0.0",
        "operational_tier": "PREMIUM",
        "total_findings": 1,
        "findings": [
            {
                "id": "bettercap_session",
                "timestamp": str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                "module": "interactive_shell",
                "finding_type": "manual_terminal_session",
                "title": "Fusion-AI Interactive Shell — Live Matrix Core",
                "severity": "INFO",
                "description": "[FUSION-AI] Persistent shell ready. Awaiting operational input command sequence...\n",
                "remediation": "Global interactive operator terminal stream. Execution scope remains fully authorized.",
                "terminal": True,
                "terminal_raw": "[FUSION-AI] Persistent shell ready. Awaiting operational input command sequence...\n",
                "session_id": "bettercap_session",
                "active": True
            }
        ],
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

    engine = FusionEngine()
    loader = PluginLoader()
    risk_engine = RiskEngine()
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
    print(" [9] Wireless Offensive & MitM Matrix (Airgeddon/Bettercap/Wifite)")

    print("-" * 60)
    
    try:
        choice = input("Opción: ").strip()


    except (KeyboardInterrupt, EOFError):
        print("\n[-] Operational cancellation received. Aborting.")
        sys.exit(0)
    # ================================================================
    # 📡 ADVANCED INTERACTIVE WIRELESS MATRIX CORE (OPTION 9)
    # ================================================================
    if choice == "9":
        print("\n" + "═" * 60)
        print(" 📡 FUSION-AI // RUNNING ADVANCED WIRELESS OFFENSIVE SUITE")
        print("═" * 60)
        
        # Invocamos tu suite inalámbrica interactiva de forma aislada
        wireless_suite.run()
        
        print("\n[✓] Wireless Operations completed. Returning to orchestrator.")
        import sys
        sys.exit(0)

    os.environ["FUSION_AUDIT_MODE"] = "HOME" if choice == "4" else "ENTERPRISE"
    
    if os.environ["FUSION_AUDIT_MODE"] == "HOME":
        print("[*] COGNITIVE VECTOR ACCEPTS -> Initializing Home Security Assessment (Full 65K Matrix).")
    else:
        print("[*] COGNITIVE VECTOR ACCEPTS -> Loading Standard Enterprise Pipeline Posture.")

    # ================================================================
    # 📡 BYPASS AUTOMÁTICO PARA VECTORES INALÁMBRICOS (0, 8 y 9)
    # ================================================================
    if choice in ["0", "8", "9"]:
        # Si el operador seleccionó cualquier matriz de radiofrecuencia,
        # forzamos el target a "0" automáticamente para encender el radar
        target = "0"
        print(f"\n[*] FUSION MATRIX -> Wireless Operational Profile [{choice}] detected.")
        print("[*] AUTOROUTING GATEWAY: Initializing frequency scanning radar loop...")
    else:
        # Bloque original intacto para escaneos de red normales (Opciones 1 a 7)
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
            print(f"\n[+] Active connection: {active_network.get('connection')}")

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

        target = wifi_result.get("target")

        if not target:
            print("\n[⚠] Wireless Exploration Matrix: No routing targets defined by module.")
            print("[i] Injecting diagnostic loopback target to maintain pipeline continuum.")
            target = "127.0.0.1"

        print(f"\n[🎯] Pipeline target resolved for Fusion core: {target}")
    # Si el operador seleccionó la Opción 9, heredamos el target y lanzamos la suite
    if choice == "9":
        print("\n" + "═" * 60)
        print(" 📡 FUSION-AI // LINKING TARGET TO ADVANCED WIRELESS SUITE")
        print("═" * 60)
        
        # Lanzamos tu suite pasándole el contexto de la red seleccionada
        wireless_suite.run()
        
        print("\n[✓] Wireless Operations completed. Returning to orchestrator.")
        import sys
        sys.exit(0)


    if not target:
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

    # ================================================================
    # DISPATCHER VECTOR FOR ADVANCED WIRELESS SUITE (OPTION 9)
    # ================================================================
    if choice == "9":
        print("\n" + "═" * 60)
        print(" 📡 FUSION-AI // RUNNING ADVANCED WIRELESS OFFENSIVE SUITE")
        print("═" * 60)
        
        # Ejecutamos el módulo autónomo de forma aislada
        wireless_suite.run()
        
        print("\n[✓] Wireless Operations completed. Returning to orchestrator.")
        import sys
        sys.exit(0)


    print("[*] CONTROL GATEWAY -> Dispatched automatic browser initialization thread...")
    trigger_automated_browser_gateway()

    scan_report = engine.run_pipeline(target)

    reconstructed = ScanContext(target)
    
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

    if "vulnerabilities" in scan_report:
        reconstructed.asset.vulnerabilities = scan_report["vulnerabilities"]
    else:
        for f in scan_report.get("findings", []):
            if f["type"] in ["vulnerability", "sql_injection"]:
                reconstructed.asset.vulnerabilities.append({
                    "name": f["title"].replace("Nuclei: ", ""),
                    "severity": str(f["severity"]).split(".")[-1].lower(),
                    "matched_at": f.get("url", target),
                    "template": f.get("data", {}).get("template_id", "unknown")
                })

    risk = risk_engine.evaluate_context(reconstructed)
    scan_report["risk_intelligence"] = risk
    scan_report["created"] = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    # ================================================================
    # STAGED AUTONOMOUS NETWORK AWARENESS DISCOVERY ENGINE (CORREGIDO)
    # ================================================================
    detected_attack_platform = None

    # Step 1: PRIORIDAD INTEGÉRRIMA - Linux Kernel routing table lookup para el TARGET específico
    if not detected_attack_platform:
        try:
            # Preguntamos al kernel por qué interfaz física real va a enrutar hacia el objetivo
            _route_dump = subprocess.check_output(f"ip route get {target}", shell=True, text=True)
            if "src" in _route_dump:
                _parts = _route_dump.split("src")
                if len(_parts) > 1:
                    # Limpiamos correctamente la IP aislándola de los caracteres restantes
                    detected_attack_platform = _parts[1].split()[0].strip()
        except Exception:
            pass

    # Step 2: Fallback routing lookup via primary public DNS sockets
    if not detected_attack_platform:
        try:
            import socket as _socket
            _s = _socket.socket(_socket.AF_INET, _socket.SOCK_DGRAM)
            _s.connect(("8.8.8.8", 80))
            detected_attack_platform = _s.getsockname()[0]
            _s.close()
        except Exception:
            pass

    # Step 3: Fallback routing lookup via secondary corporate DNS sockets
    if not detected_attack_platform:
        try:
            import socket as _socket
            _s = _socket.socket(_socket.AF_INET, _socket.SOCK_DGRAM)
            _s.connect(("1.1.1.1", 80))
            detected_attack_platform = _s.getsockname()[0]
            _s.close()
        except Exception:
            pass

    # Step 4: Final air-gapped system isolation fallback to native localhost loopback
    if not detected_attack_platform:
        detected_attack_platform = "127.0.0.1"

    # ================================================================
    # MOTOR DE DETECCIÓN DE SISTEMA OPERATIVO ATACANTE (NATIVO KALI)
    # ================================================================
    detected_attacker_os = platform.system()
    if detected_attacker_os == "Linux":
        try:
            with open("/etc/os-release", "r") as _os_f:
                _os_content = _os_f.read()
                _os_match = re.search(r'PRETTY_NAME="([^"]+)"', _os_content)
                if _os_match:
                    detected_attacker_os = _os_match.group(1)
        except Exception:
            detected_attacker_os = "Kali GNU/Linux Rolling"

    # ================================================================
    # UNIFIED GLOBAL TELEMETRY STRUCTURAL CONTRACT
    # ================================================================
    scan_report["target"] = target
    scan_report["attacker"] = detected_attack_platform
    scan_report["attacker_platform"] = detected_attack_platform
    scan_report["attacker_os"] = detected_attacker_os

    # Commit the fully parsed dynamic report ledger to local json database logs
    try:
        archive_pipeline_report(scan_report)
        with open("outputs/report.json", "w", encoding="utf-8") as ui_f:
            json.dump(scan_report, ui_f, indent=4, ensure_ascii=False)
    except Exception:
        pass

    # ================================================================
    # CENTRALIZED SYNC HANDSHAKE SUCCESS DISPLAY
    # ================================================================
    print("\n" + "=" * 60)
    print(" [✓] FUSION-AI PIPELINE WORKFLOW COMPLETE")
    print(" [●] Cyberpunk Real-Time HTML Dashboard Initialized: outputs/*")
    print(" [■] Global JSON Ledger successfully committed to database logs.")
    print("=" * 60 + "\n")

    print("\n" + "=" * 60)
    print(json.dumps(scan_report, indent=4, ensure_ascii=False))
    print("=" * 60 + "\n")

if __name__ == "__main__":
    main()
