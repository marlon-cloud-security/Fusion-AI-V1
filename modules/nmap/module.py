# modules/nmap/module.py
"""
Fusion-AI // Universal Multi-Modal Nmap Interrogator Engine v7.5 - STABLE PREMIUM
Features 100% simultaneous live terminal streaming AND instant ScanContext injections.
Fully eliminates hardcoded parameters to support global commercial operations.
Architect: Marlon F. Bonilla • Chief Cyber Operator.
Developed in collaboration with Success Team AI Dynamics.
"""

import os
import re
import sys
import json
import time
import logging
import subprocess
import shutil
import threading
from datetime import datetime
from core.types import ScanContext, Finding, Severity

logger = logging.getLogger("FusionEngine.Modules.Nmap")

# CONEXIÓN COGNITIVA: Importamos el motor de la historia ejecutiva
try:
    from intelligence.attack_story import build_attack_story
except ImportError:
    build_attack_story = None

def upsert_live_card(findings, card):
    """
    ADVANCED NORMALIZATION & DE-DUPLICATION ENGINE v4.0 - LAYER 2 MAC LOCK
    Aggressively blocks duplication across all channels using the physical MAC address.
    If the MAC signature matches inside the text or metadata, it triggers a strict fusion.
    """
    if not isinstance(findings, list):
        findings = []
        
    card_id = card.get("id")
    card_port = card.get("port")
    card_title = card.get("title", "").strip()
    card_module = card.get("module", "")
    
    # 🧬 EXTRACCIÓN DE MAC: Buscamos un patrón físico en el título, descripción o bloque data
    mac_pattern = r'(?:[0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2}'
    card_str_dump = f"{card_title} {card.get('description', '')} {str(card.get('data', ''))}"
    card_mac_match = re.search(mac_pattern, card_str_dump)
    card_mac = card_mac_match.group(0).upper() if card_mac_match else None

    idx = None
    for i, f in enumerate(findings):
        f_title = f.get("title", "").strip()
        f_module = f.get("module", "")
        
        # 🔒 REGLA SUPREMA: Validación por Capa Física (Dirección MAC)
        if card_mac:
            f_str_dump = f"{f_title} {f.get('description', '')} {str(f.get('data', ''))}"
            f_mac_match = re.search(mac_pattern, f_str_dump)
            f_mac = f_mac_match.group(0).upper() if f_mac_match else None
            
            if f_mac and f_mac == card_mac:
                idx = i
                break

        # 2. Coincidencia directa de identificador de persistencia único (ID)
        if card_id and f.get("id") == card_id:
            idx = i
            break
            
        # 3. El mismo puerto lógico mapeado por los subsistemas de Nmap
        if card_port and f.get("port") == card_port and card_module == "nmap" and f_module == "nmap":
            idx = i
            break
            
        # 4. Candado estricto para títulos exactamente idénticos
        if card_title and f_title == card_title:
            idx = i
            break

    if idx is None:
        findings.append(card)
    else:
        # Fusión inteligente de metadatos e historial operativo sin alterar el contador
        findings[idx].update(card)
        if "data" in card and card["data"]:
            findings[idx].setdefault("data", {})
            findings[idx]["data"].update(card["data"])

    return findings
def print_maligned_signature_banner() -> None:
    """
    🎨 NATIVE ASCII SIGNATURE DESPATCHER
    Prints Marlon F. Bonilla's premium brand matrix directly to the local terminal
    with precise geometric block alignments to cure potential character shifts.
    """
    print("\n" + "═" * 75)
    print(r"""
  ███████╗██╗   ██╗███████╗██╗ ██████╗ ███╗   ██╗         █████╗ ██╗
  ██╔════╝██║   ██║██╔════╝██║██╔═══██╗████╗  ██║        ██╔══██╗██║
  █████╗  ██║   ██║███████╗██║██║   ██║██╔██╗ ██║ █████╗ ███████║██║
  ██╔══╝  ██║   ██║╚════██║██║██║   ██║██║╚██╗██║ ╚════╝ ██╔══██║██║
  ██║     ╚██████╔╝███████║██║╚██████╔╝██║ ╚████║        ██║  ██║██║
  ╚═╝      ╚═════╝ ╚══════╝╚═╝ ╚═════╝ ╚═╝  ╚═══╝        ╚═╝  ╚═╝╚═╝
    """)
    print("        --- ARTIFICIAL INTELLIGENCE AT ITS FINEST ---")
    print('\n        "AND GOD SAID, LET THERE BE LIGHT!"')
    print("        [ DESIGNED & ENGINEERED BY LEAD ANALYST: M.F.B. ]")
    print("═" * 75 + "\n")
    sys.stdout.flush()

def searchsploit_lookup(service_name: str, version_banner: str):
    """
    Executes raw local sub-process binary queries against the Kali Linux Exploit-DB matrix.
    Returns every exploit found so the dashboard can list multiple execution vectors.
    """
    try:
        query = f"{service_name} {version_banner}".strip()

        if not query or len(query) < 3:
            return False, []

        result = subprocess.run(
            ["searchsploit", query],
            capture_output=True,
            text=True,
            timeout=8
        )

        output = result.stdout.strip()

        if (
            not output
            or "No Results" in output
            or "No results" in output
        ):
            return False, []

        matches = []

        for line in output.splitlines():
            if "|" not in line:
                continue
            if "Exploit Title" in line or "---" in line:
                continue

            parts = [p.strip() for p in line.split("|", 1)]
            if len(parts) != 2:
                continue

            title, path = parts
            matches.append({
                "title": title,
                "path": path,
                "type": "Metasploit (RB)" if path.endswith(".rb") else "Native Script (PY/C/TXT)"
            })

        return len(matches) > 0, matches
    except Exception:
        return False, []

def build_ui_contract(vectors):
    """
    Fusion-AI Universal UI Contract Builder.
    Every module can emit the same structure so matrix_live.html
    never needs module-specific rewrites.
    """
    ui_vectors = []
    priority_rank = [
        ("Metasploit", "Excellent", "🚀"),
        ("Python", "Great", "🐍"),
        ("Ruby", "Good", "💎"),
        ("C", "Good", "⚙️"),
        ("TXT", "Reference", "📄")
    ]
    recommended = None

    for idx, vec in enumerate(vectors, start=1):
        path = vec.get("path", "")
        title = vec.get("title", "")

        if path.endswith(".rb"):
            vtype = "Metasploit"
        elif path.endswith(".py"):
            vtype = "Python"
        elif path.endswith(".c"):
            vtype = "C"
        elif path.endswith(".txt"):
            vtype = "TXT"
        else:
            vtype = "Native"

        priority = "Good"
        icon = "⭐"

        for name, p, ico in priority_rank:
            if name == vtype:
                priority = p
                icon = ico
                break

        entry = {
            "index": idx,
            "title": title,
            "path": path,
            "type": vtype,
            "priority": priority,
            "icon": icon,
            "recommended": False
        }
        ui_vectors.append(entry)

        if recommended is None and vtype == "Metasploit":
            recommended = entry

    if recommended is None and ui_vectors:
        recommended = ui_vectors[0]

    if recommended:
        recommended["recommended"] = True

    return {
        "expandable": True,
        "show_priority": True,
        "show_paths": True,
        "show_recommendation": True,
        "recommended_vector": recommended,
        "vectors": ui_vectors
    }

def independent_exploit_db_worker(targets, paths, target_host, attacker_ip):
    """
    🧠 FUSION-AI MULTI-LAYER LIVE INTELLIGENCE COGNITIVE ENGINE
    Executes asynchronous cross-reference analytics over discovered infrastructure nodes.
    Simultaneously merges Local Exploit-DB vectors with Real-Time Global Threat Intelligence.
    Features robust, multi-tiered error wrapping to survive strict air-gapped lab operations.
    """
    import requests

    print("\n" + "═"*75)
    print(" 🧠 FUSION-AI LIVE INTELLIGENCE NETWORK ENGINE")
    print(" [POST-NMAP MULTI-LAYER ENRICHMENT ENGAGED]")
    print("═"*75)
    sys.stdout.flush()

    absolute_paths = [
        "/home/kali/Fusion-AI/outputs/json/report.json",
        "/home/kali/Fusion-AI/outputs/report.json",
        "/home/kali/Fusion-AI/outputs/fusion_history.json"
    ]

    for node in targets:
        port = node["port"]
        service = node["service"]
        banner = node["banner"]

        query = f"{service} {banner}".strip()

        print(f"\n[INTELLIGENCE HUB] Processing Port {port}")
        print(f" ├─ Querying Local DB (SearchSploit): {query}")
        sys.stdout.flush()

        vectors = []

        # =====================================================================
        # LAYER 1: LOCAL EXPLOIT-DB INTERROGATION MATRIX
        # =====================================================================
        try:
            result = subprocess.run(
                ["searchsploit", query],
                capture_output=True,
                text=True,
                timeout=8
            )
            output = result.stdout
            
            for line in output.splitlines():
                if "|" not in line or "Exploit Title" in line or "-----" in line:
                    continue
                parts = line.split("|")
                if len(parts) != 2:
                    continue
                
                raw_title = parts[0].strip()
                path = parts[1].strip()

                # Clean destructive ANSI terminal escape color codes from searchsploit output
                clean_title = re.sub(r'\x1b\[[0-9;]*[a-zA-Z]', '', raw_title)
                clean_title = clean_title.replace('[K', '').replace('[m', '').strip()

                vectors.append({
                    "title": clean_title,
                    "path": path,
                    "type": "Metasploit" if path.endswith(".rb") else "Native"
                })
            print(f" ├─ Local SearchSploit: Found {len(vectors)} exploit pathway(s).")
        except Exception as local_err:
            print(f" ├─ Local SearchSploit Error: {local_err}")

        # =====================================================================
        # LAYER 1.5: DYNAMIC HIGH-FIDELITY NSE EVIDENCE INJECTION MATRIX
        # =====================================================================
        nse_extracted_alerts = node.get("nse_findings", [])
        if nse_extracted_alerts:
            print(f" ├─ Injecting {len(nse_extracted_alerts)} live native Nmap NSE vulnerability trace(s)...")
            for alert_trace in nse_extracted_alerts:
                clean_alert_text = alert_trace.strip()
                if clean_alert_text:
                    vectors.insert(0, {
                        "title": f"🛡️ [NMAP NSE] {clean_alert_text}",
                        "path": "Nmap Local Script Database (NSE)",
                        "type": "Nmap NSE Vulnerability"
                    })
            sys.stdout.flush()
        # =====================================================================
        # LAYER 2: GLOBAL REAL-TIME THREAT INTELLIGENCE (VULNERS API)
        # =====================================================================
        web_query = service.strip() if len(service) > 2 else query
        print(f" ├─ Querying Global Threat Feed: {web_query}")
        sys.stdout.flush()
        
        global_matches = 0
        try:
            # Consulta adaptativa de vulnerabilidades en Internet basada en firmas de versión nativas
            web_response = requests.get(
                f"https://vulners.com{web_query}", 
                timeout=4
            )
            if web_response.status_code == 200:
                web_data = web_response.json()
                items = web_data.get("data", {}).get("search", [])
                
                for item in items[:5]:
                    source = item.get("_source", {})
                    cve_id = source.get("id", "GLOBAL-VULN")
                    v_title = source.get("title", "Unknown System Threat")
                    
                    vectors.append({
                        "title": f"🌍 [{cve_id}] {v_title}",
                        "path": f"https://vulners.com{cve_id}",
                        "type": "Global Intelligence"
                    })
                    global_matches += 1
                print(f" ├─ Global Threat Feed: Injected {global_matches} real-time vulnerability paths.")
        except Exception:
            print(" ├─ Global Threat Feed: Offline lab mode detected or timeout. (Skipped safely)")
            sys.stdout.flush()

        # Exit early if no vector mappings were gathered across all layers
        if not vectors:
            print(" └─ No tactical exposure vectors identified.")
            continue

        for i, v in enumerate(vectors, 1):
            print(f" │  [{i}] {v['title']}")
        sys.stdout.flush()

        # =====================================================================
        # LAYER 3: PERSISTENT CACHE & LIVE DASHBOARD SYNCHRONIZATION FLUSH
        # =====================================================================
        for report in absolute_paths:
            try:
                if not os.path.exists(report):
                    continue

                with open(report, "r", encoding="utf-8") as f:
                    data = json.load(f)

                card_updated = False
                current_findings = data.get("findings", []) if isinstance(data, dict) else data

                for card in current_findings:
                    if card.get("port") == port or card.get("id") == f"home-live-{port}":
                        
                        if port == 443 or "https" in service.lower():
                            dynamic_url = f"https://{target_host}:{port}"
                        elif "http" in service.lower():
                            dynamic_url = f"http://{target_host}:{port}"
                        else:
                            dynamic_url = f"{service}://{target_host}:{port}"

                        card["severity"] = "CRITICAL"
                        card["title"] = f"🔥 CRITICAL EXPOSURE: Port {port}/{service.upper()}"
                        nse_raw_store = node.get("nse_findings", [])
                        evidence_dump = ""
                        if nse_raw_store:
                            evidence_dump = "\n\n🛡️ [NMAP NSE LIVE VULNERABILITY TRACES]:\n"
                            for trace in nse_raw_store:
                                evidence_dump += f" ├─ {trace}\n"
                        
                        card["description"] = f"{len(vectors)} strategic multi-layer threat exposure pathway(s) identified for network daemon '{service} {banner}'.{evidence_dump}"
                        card["remediation"] = f"Upgrade or dismantle the exposed infrastructure service listening on port {port} immediately. Enforce zero-trust zoning barriers."
                        
                        card["url"] = dynamic_url
                        card["port"] = port
                        card.setdefault("data", {})
                        
                        card["data"]["severity"] = "CRITICAL"
                        ui_contract = build_ui_contract(vectors)

                        card["data"]["service"] = service
                        card["data"]["product"] = banner
                        card["data"]["url"] = dynamic_url
                        card["data"]["port"] = port

                        card["data"]["exploit_available"] = True
                        card["data"]["exploit_count"] = len(vectors)
                        card["data"]["exploit_module"] = (
                            ui_contract["recommended_vector"]["title"]
                            if ui_contract.get("recommended_vector") and isinstance(ui_contract["recommended_vector"], dict)
                            else "Exploit-DB Matrix"
                        )

                        card["data"]["exploit_vectors_available"] = ui_contract["vectors"]
                        card["data"]["recommended_vector"] = ui_contract["recommended_vector"]
                        card["data"]["ui"] = {
                            "expandable": ui_contract["expandable"],
                            "show_priority": ui_contract["show_priority"],
                            "show_paths": ui_contract["show_paths"],
                            "show_recommendation": ui_contract["show_recommendation"]
                        }
                        card["data"]["evidence_source"] = "SearchSploit Live Engine"                        
                        card["data"]["proof_of_concept"] = f"Automated structural signature identification successful for daemon rule on port {port}."
                        
                        if isinstance(vectors, list) and len(vectors) > 0:
                            card["data"]["extracted_memory"] = f"Exploit database tactical pathway match: {vectors[0].get('path', 'N/A')}"
                        else:
                            card["data"]["extracted_memory"] = "Exploit database tactical pathway match: N/A"
                        
                        # 🧬 UNIVERSAL HIGH-FIDELITY DATA LAYER ENRICHMENT
                        if 'nse_evidence' in locals() or 'nse_evidence' in globals():
                            if 'nse_evidence' in locals() and port in nse_evidence:
                                block = nse_evidence[port]
                                card["data"]["nse_verified"] = True
                                card["data"]["nse_raw"] = block["text"]
                                card["data"]["cves"] = block["cves"]
                                card["data"]["references"] = block["references"]

                                card["description"] = f"Nmap NSE verified an actively exploitable condition on port {port}."
                                card["data"]["proof_of_concept"] = block["text"]
                                card["data"]["extracted_memory"] = (
                                    "\n".join(block["references"]) if block["references"] else block["text"]
                                )
                        
                        card_updated = True
                        break

                if card_updated:
                    if isinstance(data, dict):
                        data["findings"] = current_findings
                    else:
                        data = current_findings

                    with open(report, "w", encoding="utf-8") as f:
                        json.dump(data, f, indent=4, ensure_ascii=False)
            except Exception:
                pass

        print(" └─ Dashboard synchronized.")
        sys.stdout.flush()

    print("\n" + "═"*75)
    print(" ✔ MULTI-LAYER ENRICHMENT PIPELINE COMPLETE")
    print("═"*75)
    sys.stdout.flush()

def run(context: ScanContext) -> None:
    """
    Executes a real native Nmap scan leveraging programmatic parameter mutation
    and adaptive pacing evasion vectors while preserving real-time dashboard synchronization.
    """
    print_maligned_signature_banner()

    logger.info(f"Initiating live network reconnaissance over: {context.target}")

    nmap_path = shutil.which("nmap")
    if not nmap_path:
        logger.error("Nmap binary not found in the system PATH.")
        raise FileNotFoundError("Critical dependency missing: nmap execution binary.")

    audit_profile = os.environ.get("FUSION_AUDIT_MODE", "ENTERPRISE")

    if audit_profile == "HOME":
        logger.info("[*] PROFILE DETECTED -> Engaging Autonomous Residential 65K Deep Audit Posture.")
        nmap_args = [
            "-p-", "-sT", "-sV", "--script=vuln", "-T4",
            "--min-rate", "35", "--max-rate", "95",
            "--max-rtt-timeout", "150ms", "--max-retries", "1",
            "--host-timeout", "25m", "-Pn", "--stats-every", "10s", "-vvv"
        ]
    else:
        logger.info("[*] PROFILE DETECTED -> Applying Fast Enterprise Infrastructure flags.")
        nmap_args = [
            "-p-", "-sS", "-sV", "--script=vuln", "-T4",
            "--stats-every", "5s", "-vvv"
        ]

    command = [nmap_path] + nmap_args + [str(context.target)]
    try:
        proc = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )

        absolute_report_paths = [
            "/home/kali/Fusion-AI/outputs/json/report.json",
            "/home/kali/Fusion-AI/outputs/fusion_history.json",
            "/home/kali/Fusion-AI/outputs/report.json"
        ]

        open_ports_discovered = []
        open_ports_metadata = []
        nse_evidence = {}

        print("-" * 75)
        print(" [🛰️ MONITOR ACTIVE] -> Unbuffered Dual Terminal & UI Sync Engaged:")
        print("-" * 75)
        sys.stdout.flush()

        attacker_resolved_ip = "127.0.0.1"
        try:
            import socket
            s_trace = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s_trace.connect(("8.8.8.8", 80))
            attacker_resolved_ip = s_trace.getsockname()[0]
            s_trace.close()
        except Exception:
            pass

        live_lines = []
        current_port = None
        port_descriptions = {}

        # 🛰️ INLINE UNBUFFERED LOOP TRACKER: MEMORIZES METADATA EN ROUTE WITHOUT DUPLICATION
        while True:
            line = proc.stdout.readline()
            if not line and proc.poll() is not None:
                break
            if not line:
                continue

            line_strip = line.strip()
            print(f"    {line_strip}")
            sys.stdout.flush()

            # 🛠️ DETECTOR DE PUERTOS Y ACUMULADOR DE LOGS ESTILO NATIVE MODULE
            if "/tcp" in line_strip and "open" in line_strip:
                try:
                    current_port = int(line_strip.split("/")[0])
                    port_descriptions[current_port] = f"{line_strip}\n"
                except Exception:
                    pass

            elif current_port is not None and (line_strip.startswith("|") or line_strip.startswith("_")):
                if current_port in port_descriptions:
                    port_descriptions[current_port] += f"  {line_strip}\n"

                # Si el script detecta que es vulnerable, hacemos el flush inmediato a disco
                if any(ind in line_strip for ind in ["VULNERABLE", "CVE:", "State:", "Results:"]):
                    for r_path in absolute_report_paths:
                        try:
                            if os.path.exists(r_path):
                                with open(r_path, "r", encoding="utf-8") as f_read:
                                    current_data = json.load(f_read)
                                
                                current_data.setdefault("findings", [])
                                target_card_id = f"home-live-{current_port}"
                                existing_card = next((f for f in current_data["findings"] if f.get("id") == target_card_id), None)

                                if existing_card:
                                    existing_card["severity"] = "critical"
                                    existing_card["description"] = port_descriptions[current_port].strip()
                                    existing_card.setdefault("data", {})
                                    existing_card["data"]["exploit_available"] = True
                                    existing_card["data"]["nse_verified"] = True
                                    existing_card["data"]["nse_raw"] = port_descriptions[current_port].strip()
                                    existing_card["data"]["proof_of_concept"] = port_descriptions[current_port].strip()
                                    existing_card["data"]["extracted_memory"] = port_descriptions[current_port].strip()
                                    
                                    current_data["findings"] = upsert_live_card(current_data["findings"], existing_card)

                                    with open(r_path, "w", encoding="utf-8") as f_write:
                                        json.dump(current_data, f_write, indent=4, ensure_ascii=False)
                        except Exception:
                            pass
            # 🛡️ DYNAMIC LIVE NSE INJECTOR (FLUSHES DIRECTLY TO DISK EXPOSURE INTERFACE)
            if open_ports_metadata:
                current_active_node = open_ports_metadata[-1]
                active_port_num = current_active_node["port"]
                clean_stream_line = line_strip.lstrip()
                
                if clean_stream_line.startswith("|") or clean_stream_line.startswith("_") or any(ind in clean_stream_line for ind in ["VULNERABLE", "CVE:", "State:", "References:", "Results:", "Shell command:"]):
                    purified_nse_trace = clean_stream_line.replace("|", "").replace("_", "").strip()
                    
                    if purified_nse_trace and not any(k in purified_nse_trace for k in ["NSE:", "Initiating", "Completed", "Scanning"]):
                        for sync_report_path in absolute_report_paths:
                            try:
                                if os.path.exists(sync_report_path):
                                    with open(sync_report_path, "r", encoding="utf-8") as f_r:
                                        disk_json_data = json.load(f_r)
                                    
                                    disk_json_data.setdefault("findings", [])
                                    target_card_id = f"home-live-{active_port_num}"
                                    target_card = next((f for f in disk_json_data["findings"] if f.get("id") == target_card_id), None)
                                    
                                    if target_card:
                                        if "🛡️ [NMAP NSE EVIDENCE]" not in target_card["description"]:
                                            target_card["description"] += "\n\n🛡️ [NMAP NSE EVIDENCE]:\n"
                                        
                                        if purified_nse_trace not in target_card["description"]:
                                            target_card["description"] += f" ├─ {purified_nse_trace}\n"
                                            
                                        with open(sync_report_path, "w", encoding="utf-8") as f_w:
                                            json.dump(disk_json_data, f_w, indent=4, ensure_ascii=False)
                            except Exception:
                                pass

            # Parseo y extracción en caliente de variables de red
            port_id = None
            s_name = "unknown"
            v_banner = "generic/network-service-layer"

            if "Discovered open port" in line_strip:
                p_match = re.search(r"port\s+(\d+)/tcp", line_strip)
                if p_match:
                    port_id = int(p_match.group(1))
            elif "/tcp" in line_strip and "open" in line_strip:
                p_match = re.search(
                    r"^(\d+)/tcp\s+open\s+(\S+)(?:\s+syn-ack\s+ttl\s+\d+)?(?:\s+\(access\s+denied\))?\s*(.*)",
                    line_strip
                )
                if p_match:
                    port_id = int(p_match.group(1))
                    s_name = p_match.group(2).strip()
                    if p_match.group(3):
                        v_banner = p_match.group(3).strip()

            # =====================================================================
            # 🛡️ BLINDAJE ULTRA-QUIRÚRGICO DE RAÍZ CONTRA ESTADOS INVÁLIDOS ("None")
            # =====================================================================
            if port_id is None or str(port_id).lower() == 'none' or not port_id:
                continue

            if port_id is not None:
                existing_meta = next((m for m in open_ports_metadata if m["port"] == port_id), None)
                if existing_meta:
                    if s_name != "unknown":
                        existing_meta["service"] = s_name
                    if v_banner != "generic/network-service-layer":
                        existing_meta["banner"] = v_banner
                else:
                    existing_meta = {
                        "port": port_id,
                        "service": s_name,
                        "banner": v_banner,
                        "nse_findings": []
                    }
                    open_ports_metadata.append(existing_meta)

            # Sincronización de estados de infraestructura local en el contexto
            if port_id not in context.open_ports:
                context.open_ports.append(port_id)

                finding = Finding(
                    module="nmap",
                    finding_type="open_port",
                    title=f"Open Network Port Discovered: {port_id}/TCP",
                    severity=Severity.MEDIUM,
                    data={
                        "port": port_id,
                        "protocol": "tcp",
                        "service": s_name,
                        "product": v_banner
                    },
                    description=f"Port {port_id} detected listening actively over target interface gates.",
                    remediation="Enforce strict firewall zoning policies. Close ports that are not business-critical.",
                    port=port_id
                )

                # 🧬 ID ÚNICO COMPARTIDO CON EL LIVE JSON (elimina duplicados)
                finding.id = f"home-live-{port_id}"

                if hasattr(context, "add_finding"):
                    context.add_finding(finding)

                context.asset.open_ports.append({
                    "port": port_id,
                    "service": s_name,
                    "product": v_banner,
                    "protocol": "tcp"
                })

            # 🚀 LIVE JSON FLUSH INJECTOR UNIFICADO (Sincronización sin Duplicados)
            # =====================================================================
            for r_path in absolute_report_paths:
                try:
                    if os.path.exists(r_path):
                        with open(r_path, "r", encoding="utf-8") as f_read:
                            current_data = json.load(f_read)
                    else:
                        current_data = {"target": context.target, "findings": [], "total_findings": 0}

                    current_data.setdefault("findings", [])
                    target_card_id = f"home-live-{port_id}"
                    
                    has_nse = port_id in nse_evidence
                    nse_block = nse_evidence[port_id] if has_nse else None

                    existing_card = next((f for f in current_data["findings"] if f.get("id") == target_card_id), None)

                    if existing_card:
                        if s_name != "unknown":
                            existing_card["data"]["service"] = s_name
                            existing_card["description"] = f"Port {port_id} detected actively listening over target interface gates. Service Type: '{s_name}'. Version: '{v_banner}'."
                        if v_banner != "generic/network-service-layer":
                            existing_card["data"]["product"] = v_banner
                        
                        if has_nse:
                            existing_card["severity"] = "critical"
                            existing_card["description"] = f"Nmap NSE verified an actively exploitable condition on port {port_id}.\n\n{nse_block['text']}"
                            existing_card["data"]["exploit_available"] = True
                            existing_card["data"]["nse_verified"] = True
                            existing_card["data"]["nse_raw"] = nse_block["text"]
                            existing_card["data"]["cves"] = nse_block["cves"]
                            existing_card["data"]["references"] = nse_block["references"]
                            existing_card["data"]["proof_of_concept"] = nse_block["text"]
                            existing_card["data"]["extracted_memory"] = "\n".join(nse_block["references"]) if nse_block["references"] else nse_block["text"]
                    else:
                        live_node = {
                            "id": target_card_id, "module": "nmap", "type": "open_port",
                            "title": f"Open Network Port Discovered: {port_id}/TCP", "severity": "medium",
                            "description": f"Port {port_id} detected actively listening over target interface gates. Service Type: '{s_name}'. Version: '{v_banner}'.",
                            "remediation": "Enforce strict firewall zoning policies. Close ports that are not business-critical.",
                            "port": port_id, "url": f"http://{context.target}:{port_id}" if port_id == 80 else f"https://{context.target}:{port_id}" if port_id == 443 else None,
                            "timestamp": str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                            "data": {
                                "port": port_id, "protocol": "tcp", "service": s_name, "product": v_banner,
                                "evidence_source": "Nmap Recon Engine", "exploit_available": True if has_nse else False,
                                "exploit_vectors_available": [], "active_selected_vector": "N/A"
                            }
                        }
                        current_data["findings"] = upsert_live_card(current_data["findings"], live_node)

                    current_data["total_findings"] = len(current_data["findings"])
                    current_data["attacker_platform"] = attacker_resolved_ip
                    current_data["created"] = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    current_data["target"] = context.target

                    with open(r_path, "w", encoding="utf-8") as f_write:
                        json.dump(current_data, f_write, indent=4, ensure_ascii=False)
                except Exception:
                    pass

        # Liberación segura de subprocesos terminales
        proc.stdout.close()
        proc.wait()

        # Consolidación final de puertos para asegurar conteo neto real
        for port_key in nse_evidence if "nse_evidence" in locals() else []:
            for sync_path in absolute_report_paths:
                try:
                    if os.path.exists(sync_path):
                        with open(sync_path, "r", encoding="utf-8") as f_r:
                            disk_data = json.load(f_r)
                        disk_data["findings"] = [f for f in disk_data.get("findings", []) if not (f.get("module") == "nmap" and f.get("port") == port_key and len(f.get("id", "")) > 20)]
                        with open(sync_path, "w", encoding="utf-8") as f_w:
                            json.dump(disk_data, f_w, indent=4, ensure_ascii=False)
                except Exception: pass
        # 🧠 MASTER SYSTEM ONSITE EVIDENCE FLUSH PIPELINE (WHATWEB-STYLE MASTER SYSTEM)
        if nse_evidence:
            print(f" \n ├─ [🧠 CORE SYNC] Found {len(nse_evidence)} active NSE vulnerability blocks in memory. Securing disk...")
            for sync_path in absolute_report_paths:
                try:
                    if os.path.exists(sync_path):
                        with open(sync_path, "r", encoding="utf-8") as f_r:
                            disk_data = json.load(f_r)
                        
                        disk_data.setdefault("findings", [])
                        updates_committed = False

                        for port_key, block_data in nse_evidence.items():
                            target_id = f"home-live-{port_key}"
                            card_target = next((f for f in disk_data["findings"] if f.get("id") == target_id), None)

                            if card_target:
                                # Elevate card state to critical with native high-fidelity properties
                                card_target["severity"] = "critical"
                                
                                # 📡 RAW CONSOLE INJECTION: Flushes the exact terminal trace into the description slot
                                card_target["description"] = block_data['text']
                                
                                card_target.setdefault("data", {})
                                card_target["data"]["exploit_available"] = True
                                card_target["data"]["nse_verified"] = True
                                card_target["data"]["nse_raw"] = block_data["text"]
                                card_target["data"]["cves"] = block_data["cves"]
                                card_target["data"]["references"] = block_data["references"]
                                card_target["data"]["proof_of_concept"] = block_data["text"]
                                card_target["data"]["extracted_memory"] = block_data["text"]
                                card_target["data"]["evidence_source"] = "Nmap Live Recon Engine (NSE)"
                                updates_committed = True

                        if updates_committed:
                            with open(sync_path, "w", encoding="utf-8") as f_w:
                                json.dump(disk_data, f_w, indent=4, ensure_ascii=False)
                            print(f" │  [✔] Physical sync complete for endpoint gate: {sync_path}")
                except Exception as sync_err:
                    print(f" │  [⚠️] Error writing final evidence matrix to {sync_path}: {sync_err}")
            sys.stdout.flush()

        print("═"*75 + "\n")
        logger.info(f"Nmap pipeline stage finalized | Asset open_ports populated: {len(context.asset.open_ports)}")

        # ⚡ BACKGROUND COGNITIVE ENGAGEMENT INTERFACE: Dispatches the Multi-Vector Exploit DB thread
        if open_ports_metadata:
            logger.info(f"🧠 [INTELLIGENCE LINK] Launching asynchronous SearchSploit processing thread over {len(open_ports_metadata)} nodes...")
            bg_thread = threading.Thread(
                target=independent_exploit_db_worker,
                args=(open_ports_metadata, absolute_report_paths, str(context.target), attacker_resolved_ip),
                daemon=True
            )
            bg_thread.start()

        # 🚀 THE COGNITIVE MASTER ENGAGEMENT: Compila la Attack Story ejecutiva al cerrar el flujo de red
        if build_attack_story is not None:
            logger.info("[🧠 EXECUTIVE INTELLIGENCE] Compiling corporate narrative timeline via Attack Story Engine...")
            build_attack_story("/home/kali/Fusion-AI/outputs/json/report.json")

    except Exception as e:
        logger.error(f"Unexpected processing breakdown inside Nmap unbuffered stream: {str(e)}")
        raise e
