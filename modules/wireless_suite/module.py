# modules/wireless_suite/module.py
import logging
import os
import json
import shutil
import subprocess
import sys
import threading
import time
from datetime import datetime
from typing import Dict, Optional
from core.types import ScanContext, Finding, Severity

logger = logging.getLogger("FusionEngine.Modules.WirelessSuite")

# ============================================================
# FUSION-AI // ULTIMATE ALL-IN-ONE MILITARY ASSAULT MATRIX (OPT 9)
# ============================================================
TOOLS: Dict[str, Dict[str, str]] = {
    "1": {"name": "Airgeddon", "binary": "airgeddon", "type": "wireless_assessment"},
    "2": {"name": "Wifite", "binary": "wifite", "type": "wireless_assessment"},
    "3": {"name": "Bettercap Framework", "binary": "bettercap", "type": "network_mitm"},
    "4": {"name": "TShark Packet Analyzer", "binary": "tshark", "type": "packet_analysis"},
    "5": {"name": "Fluxion Phishing Core", "binary": "fluxion", "type": "wireless_phishing"},
    "6": {"name": "Wifiphisher Evil-Twin", "binary": "wifiphisher", "type": "wireless_rogue_ap"},
    "7": {"name": "BeEF-XSS Framework", "binary": "beef-xss", "type": "browser_exploitation"},
    "8": {"name": "EAPHammer Enterprise", "binary": "eaphammer", "type": "enterprise_wireless"},
    "9": {"name": "Kismet Stealth Radar", "binary": "kismet", "type": "wireless_monitoring"},
    "10": {"name": "Aircrack-ng Cracker", "binary": "aircrack-ng", "type": "cryptographic_validation"},
    "11": {"name": "MSFVenom Payload Wizard", "binary": "msfvenom", "type": "c2_weaponization"},
    "12": {"name": "SSTImap RCE Engine", "binary": "sstimap", "type": "web_exploitation"},
    "13": {"name": "XSStrike WAF Bypass", "binary": "xsstrike", "type": "web_vulnerability"},
    "14": {"name": "WPProbe CMS Auditor", "binary": "wpprobe", "type": "cms_enumeration"}
}

CLR_RESET = "\033[0m"
CLR_GREEN = "\033[1;32m"
CLR_CYAN = "\033[1;36m"
CLR_YELLOW = "\033[1;33m"
CLR_RED = "\033[1;31m"
CLR_WHITE = "\033[1;37m"

def print_banner() -> None:
    print()
    print(f"{CLR_CYAN}============================================================{CLR_RESET}")
    print(f"{CLR_CYAN}    FUSION-AI // ULTIMATE ADVANCED PERSISTENT THREAT MATRIX  {CLR_RESET}")
    print(f"{CLR_CYAN}============================================================{CLR_RESET}")
    print("  Unified Tactical Command Center - Military-Grade Operations")
    print("  Asynchronous Live Streaming Telemetry Array - Threaded Core")
    print("  Engineered & Standardized by Operator Leader [ M.F.B. ]")
    print(f"{CLR_CYAN}============================================================{CLR_RESET}\n")

def check_authorization() -> bool:
    print(f"{CLR_YELLOW}[!] SECURITY ENGAGEMENT CHARTER REQUIRED{CLR_RESET}")
    print("This tactical array executes high-impact operations. Written scope auth is mandatory.")
    print()
    while True:
        confirmation = input(f"{CLR_WHITE}Type AUTHORIZED to ignite the Swiss Knife Suite: {CLR_RESET}").strip().upper()
        if confirmation == "AUTHORIZED":
            print(f"\n{CLR_GREEN}[✓] Token verified successfully. Access granted.{CLR_RESET}\n")
            return True
        print(f"{CLR_RED}[❌ ERROR] Wrong authorization token! Please, type AUTHORIZED correctly.{CLR_RESET}")
def print_tactical_menu() -> None:
    status = {k: shutil.which(v["binary"]) for k, v in TOOLS.items()}
    print(f"{CLR_CYAN}================== MULTI-VECTOR OPERATIONAL ASSAULT ECOSYSTEM =================={CLR_RESET}")
    
    print(f"\n  {CLR_CYAN}[ VECTOR A: AUTOMATED & GUIDED WIRELESS ORCHESTRATION ]{CLR_RESET}")
    for k in ["1", "2"]:
        state = f"{CLR_GREEN}READY{CLR_RESET}" if status[k] else f"{CLR_RED}NOT INSTALLED{CLR_RESET}"
        print(f"    [{k:<2}] {TOOLS[k]['name']:<26} [{state}]")

    print(f"\n  {CLR_CYAN}[ VECTOR B: NETWORK INTERCEPTION & MAN-IN-THE-MIDDLE ]{CLR_RESET}")
    for k in ["3", "4"]:
        state = f"{CLR_GREEN}READY{CLR_RESET}" if status[k] else f"{CLR_RED}NOT INSTALLED{CLR_RESET}"
        print(f"    [{k:<2}] {TOOLS[k]['name']:<26} [{state}]")

    print(f"\n  {CLR_CYAN}[ VECTOR C: ROGUE AP, WIRELESS PHISHING & SOCIAL ENGINEERING ]{CLR_RESET}")
    for k in ["5", "6", "7"]:
        state = f"{CLR_GREEN}READY{CLR_RESET}" if status[k] else f"{CLR_RED}NOT INSTALLED{CLR_RESET}"
        print(f"    [{k:<2}] {TOOLS[k]['name']:<26} [{state}]")

    print(f"\n  {CLR_CYAN}[ VECTOR D: ENTERPRISE AUDITING & SIGINT MONITORING ]{CLR_RESET}")
    for k in ["8", "9", "10"]:
        state = f"{CLR_GREEN}READY{CLR_RESET}" if status[k] else f"{CLR_RED}NOT INSTALLED{CLR_RESET}"
        print(f"    [{k:<2}] {TOOLS[k]['name']:<26} [{state}]")

    print(f"\n  {CLR_CYAN}[ VECTOR E: WEB PERIMETER BREACH & WEAPONIZATION ]{CLR_RESET}")
    for k in ["11", "12", "13", "14"]:
        state = f"{CLR_GREEN}READY{CLR_RESET}" if status[k] else f"{CLR_RED}NOT INSTALLED{CLR_RESET}"
        print(f"    [{k:<2}] {TOOLS[k]['name']:<26} [{state}]")

    print(f"\n{CLR_CYAN}================================================================================{CLR_RESET}")
    print(f"    [{CLR_GREEN}0{CLR_RESET}] Return to Central Autonomous Orchestrator Menu\n")

def monitor_live_logs(
    log_path: str,
    tool_name: str,
    finding_type: str,
    context: ScanContext
) -> None:
    """
    Mirror the native tool output into one persistent Fusion-AI session.

    Raw ANSI terminal sequences are preserved intentionally.
    """

    time.sleep(1.0)

    if not os.path.exists(log_path):
        return

    module_key = tool_name.lower().replace(" ", "_")
    session_id = f"{module_key}_session"

    absolute_paths = [
        "/home/kali/Fusion-AI/outputs/json/report.json",
        "/home/kali/Fusion-AI/outputs/report.json",
    ]

    raw_terminal = []

    try:
        with open(
            log_path,
            "r",
            encoding="utf-8",
            errors="ignore"
        ) as stream:

            stream.seek(0)

            while os.environ.get(
                "FUSION_SUBPROCESS_ACTIVE"
            ) == "TRUE":

                line = stream.readline()

                if not line:
                    time.sleep(0.15)
                    continue

                # Preserve the native Bettercap terminal stream.
                raw_terminal.append(line)

                terminal_content = "".join(raw_terminal)

                session_finding = {
                    "id": session_id,
                    "timestamp": datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                    "module": module_key,
                    "finding_type": "manual_terminal_session",
                    "title": f"{tool_name} — Live Terminal Session",

                    # Manual terminal sessions are telemetry,
                    # not vulnerabilities by themselves.
                    "severity": "LOW",

                    # Keep ANSI untouched.
                    "description": terminal_content,

                    "remediation": (
                        "Manual operator session. "
                        "Review observed telemetry and validate "
                        "findings against the authorized scope."
                    ),

                    "terminal": True,
                    "terminal_raw": terminal_content,
                    "session_id": session_id,
                    "active": True,
                }

                # ========================================================
                # Persist exactly ONE session card.
                # ========================================================
                for target_path in absolute_paths:

                    os.makedirs(
                        os.path.dirname(target_path),
                        exist_ok=True
                    )

                    current_report = {}

                    if (
                        os.path.exists(target_path)
                        and os.path.getsize(target_path) > 0
                    ):
                        try:
                            with open(
                                target_path,
                                "r",
                                encoding="utf-8"
                            ) as rf:
                                current_report = json.load(rf)

                        except Exception:
                            current_report = {}

                    if not isinstance(current_report, dict):
                        current_report = {}

                    current_report["status"] = "ONLINE"
                    current_report["timestamp"] = datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )

                    current_report.setdefault(
                        "target",
                        getattr(context, "target", "")
                    )

                    current_report.setdefault(
                        "attacker",
                        ""
                    )

                    current_report.setdefault(
                        "os",
                        "Kali GNU/Linux Rolling"
                    )

                    if not isinstance(
                        current_report.get("findings"),
                        list
                    ):
                        current_report["findings"] = []

                    # ====================================================
                    # Remove every previous manual terminal session
                    # belonging to this tool.
                    #
                    # This is important when the operator launches
                    # Bettercap again during the same Fusion-AI lifetime.
                    # ====================================================
                    current_report["findings"] = [
                        finding
                        for finding in current_report["findings"]
                        if not (
                            finding.get("module") == module_key
                            and finding.get(
                                "finding_type"
                            ) == "manual_terminal_session"
                        )
                    ]

                    # Add ONE current terminal session.
                    current_report["findings"].append(
                        session_finding
                    )

                    current_report["total_findings"] = len(
                        current_report["findings"]
                    )

                    current_report["high_exploits"] = len([
                        finding
                        for finding in current_report["findings"]
                        if finding.get("severity") == "HIGH"
                    ])

                    current_report["medium_breaches"] = len([
                        finding
                        for finding in current_report["findings"]
                        if finding.get("severity") == "MEDIUM"
                    ])

                    current_report["devices_discovered"] = 0

                    with open(
                        target_path,
                        "w",
                        encoding="utf-8"
                    ) as wf:

                        json.dump(
                            current_report,
                            wf,
                            indent=4,
                            ensure_ascii=False
                        )

                # ========================================================
                # Existing Fusion-AI live synchronization bus.
                #
                # One logical Finding for the whole manual session.
                # ========================================================
                try:

                    context.add_finding(
                        Finding(
                            module=module_key,
                            finding_type="manual_terminal_session",
                            title=(
                                f"{tool_name} "
                                f"— Live Terminal Session"
                            ),
                            severity=Severity.LOW,

                            data={
                                "session_id": session_id,
                                "terminal": True,
                                "raw_stream_length": len(
                                    terminal_content
                                ),
                            },

                            description=terminal_content,

                            remediation=(
                                "Manual operator session. "
                                "Review observed telemetry and "
                                "validate findings against "
                                "the authorized scope."
                            ),
                        )
                    )

                except Exception as sync_error:

                    logger.debug(
                        "Terminal session live sync: %s",
                        sync_error
                    )

    except Exception as error:

        logger.error(
            "Terminal stream error for %s: %s",
            tool_name,
            error
        )
def launch_native_tool(context: ScanContext, tool_key: str) -> None:
    tool = TOOLS.get(tool_key)
    if not tool: return
    binary, tool_name, finding_type = tool["binary"], tool["name"], tool["type"]
    executable = shutil.which(binary)

    if not executable:
        print(f"\n{CLR_RED}[❌ TACTICAL ERROR]{CLR_RESET} Binary for {tool_name} is missing.\n")
        return

    log_dir = "outputs/logs"
    os.makedirs(log_dir, exist_ok=True)
    session_log = os.path.join(log_dir, f"fusion_{binary}_stream.log")
    if os.path.exists(session_log):
        try: os.remove(session_log)
        except: pass

    with open(session_log, "w", encoding="utf-8") as f:
        f.write("")

    # Orquestación de caplets y tubería tee nativa interactiva para volcado transparente
    runtime_cmd = executable
    if binary == "bettercap":
        caplet_path = os.path.join(log_dir, "fusion_auto.cap")
        with open(caplet_path, "w", encoding="utf-8") as cap:
            cap.write("net.probe on\n")
            cap.write("clear\n")
        runtime_cmd = f"{executable} -caplet {caplet_path} | tee -a {session_log}"
    
    print(f"\n{CLR_GREEN}[🚀 DEPLOYING]{CLR_RESET} Executing interactive sub-shell for {tool_name}...\n")
    try:
        os.environ["FUSION_SUBPROCESS_ACTIVE"] = "TRUE"

        monitor_thread = threading.Thread(
            target=monitor_live_logs,
            args=(session_log, tool_name, finding_type, context),
            daemon=True
        )
        monitor_thread.start()

        # Lanzamiento interactivo puro conservando eco del teclado y visibilidad total
        try:
            process_result = subprocess.run(
                runtime_cmd,
                shell=True,
                stdin=sys.stdin,
                stdout=sys.stdout,
                stderr=sys.stderr
            )
            
            os.environ["FUSION_SUBPROCESS_ACTIVE"] = "FALSE"
            return_code = process_result.returncode
            print(f"\n{CLR_CYAN}[i]{CLR_RESET} Operational module {tool_name} closed safely. Exit code: {return_code}.\n")
        except KeyboardInterrupt:
            os.environ["FUSION_SUBPROCESS_ACTIVE"] = "FALSE"
            print(f"\n{CLR_YELLOW}[⚠ SIGNAL INTERRUPT]{CLR_RESET} Returning to local matrix safely...")
        def command_injection_listener(proc_handle):
            ipc_signal_file = "outputs/logs/terminal_stdin.txt"
            while proc_handle.poll() is None:
                try:
                    if os.path.exists(ipc_signal_file):
                        time.sleep(0.05)  # Tiny stabilization window for file lock avoidance
                        with open(ipc_signal_file, "r", encoding="utf-8") as sig_f:
                            incoming_cmd = sig_f.read().strip()
                        
                        if incoming_cmd:
                            # Deliver the keystroke data array into the active Kali process stdin core
                            proc_handle.stdin.write(f"{incoming_cmd}\n".encode("utf-8"))
                            proc_handle.stdin.flush()
                        
                        # Discard the processed signal marker to welcome the next command sequence
                        os.remove(ipc_signal_file)
                except Exception:
                    pass
                time.sleep(0.1)

        # Instantiate and ignite the isolated background pipeline tracking task thread
        signal_worker = threading.Thread(
            target=command_injection_listener,
            args=(process_result,),
            daemon=True
        )
        signal_worker.start()

        # Securely lock the localized execution context until the process naturally terminates
        while process_result.poll() is None:
            time.sleep(0.5)

        os.environ["FUSION_SUBPROCESS_ACTIVE"] = "FALSE"
        return_code = process_result.returncode
        print(f"\n{CLR_CYAN}[i]{CLR_RESET} Operational module {tool_name} closed safely. Exit code: {return_code}.\n")
    except KeyboardInterrupt:
        os.environ["FUSION_SUBPROCESS_ACTIVE"] = "FALSE"
        print(f"\n{CLR_YELLOW}[⚠ SIGNAL INTERRUPT]{CLR_RESET} Returning to local matrix safely...")

def run(context: Optional[ScanContext] = None) -> None:
    if context is None:
        context = ScanContext("integrated_assault_profile")
    print_banner()
    if not check_authorization(): return
    while True:
        print_tactical_menu()
        choice = input(f"{CLR_WHITE}Select operation index: {CLR_RESET}").strip()
        if choice == "0":
            print(f"\n{CLR_GREEN}[✓]{CLR_RESET} Demobilizing assault matrix. Re-aligning orchestrator core...\n")
            return
        if choice in TOOLS:
            launch_native_tool(context, choice)
        else:
            print(f"\n{CLR_RED}[❌ ERROR] Target index invalid.{CLR_RESET}\n")

if __name__ == "__main__":
    run()

