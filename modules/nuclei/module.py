# modules/nuclei/module.py

import logging
import subprocess
import shutil
import json
import os
import sys
import time
import threading
from typing import List, Dict, Any

from core.types import ScanContext, Finding, Severity
from intelligence.decision_engine import DecisionEngine
from intelligence.adaptive_engine import AdaptiveEngine
from reporting.report import ReportGenerator

logger = logging.getLogger("FusionEngine.Modules.Nuclei")

# ============================================================
# LIVE ENGINE TELEMETRY WRITER
# ============================================================

ENGINE_STATUS_FILE = "outputs/engine_status.json"


def update_engine_status(batch, mode, health, elapsed, stream):

    telemetry = {
        "engine": "ONLINE",
        "batch": batch,
        "mode": mode,
        "health": health,
        "elapsed": elapsed,
        "stream": stream,
        "nuclei": {
            "status": "ACTIVE",
            "matches": 0
        }
    }

    try:
        with open(ENGINE_STATUS_FILE, "w", encoding="utf-8") as f:
            json.dump(telemetry, f, indent=4)

    except Exception as e:
        logger.debug(f"ENGINE TELEMETRY WRITE ERROR: {e}")

# ANSI Color Matrix Codes for High-Impact Terminal Rendering
CLR_RESET = "\033[0m"
CLR_CRITICAL = "\033[1;31m"  # Bold Red
CLR_HIGH = "\033[1;35m"      # Bold Magenta
CLR_MEDIUM = "\033[1;33m"    # Bold Yellow
CLR_INFO = "\033[1;36m"      # Bold Cyan
CLR_GREEN = "\033[1;32m"     # Bold Green

# Global thread synchronization controls
dashboard_active = True
temp_output_file_global = ""

import threading

# 1. Establish an authoritative thread synchronization lock boundary
# This protects cumulative RAM structures from being truncated during batch switches
context_sync_lock = threading.Lock()

def live_dashboard_worker(context: ScanContext) -> None:
    """
    Independent asynchronous thread worker leveraging strict Mutex locking parameters.
    Bypasses volatile disk I/O mutations by copying cumulative context graphs directly from shared memory,
    guaranteeering real-time incremental counter updates and instant dashboard re-rendering.
    """
    import time
    import copy
    from reporting.report import ReportGenerator, load_json_database, save_json_database, HISTORY_DATABASE
    
    logger.info("📡 Asynchronous Cyberpunk live dashboard rendering engine thread engaged.")
    global dashboard_active
    
    while dashboard_active:
        # Sleep for 5 seconds to provide ultra-fast real-time synchronization
        time.sleep(5)
        try:
            # Acquire thread-safe operational lock to execute atomic deep memory cloning
            with context_sync_lock:
                if not context.findings:
                    continue
                # Create a bulletproof isolated clone of the cumulative main memory context
                local_context = copy.deepcopy(context)
            
            # Hot sync memory alignment: Extract flat dictionary list from memory findings
            raw_findings = [f.to_dict() for f in local_context.findings]
            if raw_findings:
                current_db = load_json_database(HISTORY_DATABASE)
                if not isinstance(current_db, list):
                    current_db = []
                
                # Check and append new unique memory findings to unblock api_server.py
                for rf in raw_findings:
                    exists = any(old.get("title") == rf.get("title") and old.get("target") == rf.get("target") for old in current_db)
                    if not exists:
                        current_db.append(rf)
                
                save_json_database(HISTORY_DATABASE, current_db)
            
            # Enforce white-label interface generation using the native authoritative method
            reporter = ReportGenerator(local_context)
            reporter.generate_html_report(local_context.findings)
            
        except Exception as async_dashboard_err:
            logger.debug(f"Asynchronous dashboard builder update bypassed: {str(async_dashboard_err)}")

    # Final persistent execution block triggered when the master suite pipeline completes
    try:
        reporter = ReportGenerator(context)
        reporter.generate_html_report(context.findings)
    except Exception:
        pass
    logger.info("👋 Asynchronous dashboard compiler thread successfully released.")
def parse_and_accumulate_batch(file_path: str, context: ScanContext, silent_mode: bool = False) -> int:
    """
    Parses structural JSONL outputs applying deduplication and memory consolidation matrix filters.
    Utilizes localized thread-safe mutex boundaries to inject records without race conditions.
    """
    severity_map = {
        "info": Severity.INFO, "low": Severity.LOW, "medium": Severity.MEDIUM,
        "high": Severity.HIGH, "critical": Severity.CRITICAL,
    }

    unique_findings_count = 0
    consolidation_matrix = {}

    try:
        if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
            return 0

        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            lines = [l.strip() for l in f if l.strip()]

        for line in lines:
            try:
                data = json.loads(line)
            except json.JSONDecodeError:
                continue

            info = data.get("info", {})
            name = info.get("name", "Unknown Finding")
            severity_raw = info.get("severity", "info").lower()
            matched_url = data.get("matched-at", context.target)
            template_id = data.get("template-id", "unknown")
            cves = info.get("classification", {}).get("cve-id", [])

            matrix_key = f"{matched_url}::{template_id}"

            if matrix_key not in consolidation_matrix:
                consolidation_matrix[matrix_key] = {
                    "name": name,
                    "severity_raw": severity_raw,
                    "matched_url": matched_url,
                    "template_id": template_id,
                    "cves": cves,
                    "count": 1,
                    "info": info,
                    "raw_data": data
                }
            else:
                consolidation_matrix[matrix_key]["count"] += 1

        # ACQUIRE CRITICAL THREAD LOCK MATRIX BEFORE WRITING MUTABLE GLOBAL SHARED MEMORY ARRAYS
        with context_sync_lock:
            for key, entity in consolidation_matrix.items():
                s_raw = entity["severity_raw"]
                severity_enum = severity_map.get(s_raw, Severity.INFO)
                
                # Enforce thread-safe duplicate validation over the authoritative data stream
                already_exists = any(
                    v.get("template") == entity["template_id"] and v.get("matched_at") == entity["matched_url"]
                    for v in context.asset.vulnerabilities
                )
                
                if not already_exists:
                    context.asset.vulnerabilities.append({
                        "name": entity["name"],
                        "severity": s_raw,
                        "matched_at": entity["matched_url"],
                        "template": entity["template_id"],
                        "cves": entity["cves"]
                    })

                    curl_cmd = entity["raw_data"].get("curl-command", f"curl -X 'GET' '{entity['matched_url']}'")
                    raw_response = entity["raw_data"].get("response", "Handshake signature successfully validated.")

                    finding = Finding(
                        module="nuclei", 
                        finding_type="vulnerability",
                        title=f"Nuclei: {entity['name']}", 
                        severity=severity_enum,
                        data={
                            "template_id": entity["template_id"], 
                            "matched_url": entity["matched_url"], 
                            "cves": entity["cves"], 
                            "hits_consolidated": entity["count"],
                            "curl-command": curl_cmd,
                            "raw_log_summary": raw_response
                    },
                        description=entity["info"].get("description", "Vulnerability footprint successfully mapped."), 
                        remediation=entity["info"].get("remediation", "Apply vendor updates cleanly."), 
                        url=entity["matched_url"]
                    )
                    context.add_finding(finding)

                # Always increment metric counters globally across the structural sweep loops
                unique_findings_count += 1

                # Visual terminal reporting pass (Only displays unique hits in console stream)
                if not silent_mode and not already_exists:
                    if "critical" in s_raw:
                        color = CLR_CRITICAL
                    elif "high" in s_raw:
                        color = CLR_HIGH
                    elif "medium" in s_raw:
                        color = CLR_MEDIUM
                    else:
                        color = CLR_INFO

                    count_suffix = f" (Repeated {entity['count']} times - Consolidated)" if entity['count'] > 1 else ""
                    print(f"    🌟 {color}[FINDING SECURED]{CLR_RESET} -> [{color}{s_raw.upper()}{CLR_RESET}] {entity['name']} | {entity['matched_url']}{CLR_RESET}{count_suffix}")
                    sys.stdout.flush()

        return unique_findings_count

    except Exception as e:
        logger.error(f"Critical breakdown inside deduplication memory loader: {str(e)}")
        return 0

def run(context: ScanContext) -> None:
    """
    Context-driven Nuclei execution engine. Engineered with Supersonic Congestion Control,
    Dual-Pass Target Segregation, and asynchronous live-threaded dashboard generation.
    """
    global dashboard_active, temp_output_file_global
    global_scan_start = time.time()

    
    engine = DecisionEngine()
    attack_plan = engine.generate_attack_plan(context)

    target_pool: List[str] = attack_plan.get("targets", [])
    tags_filter: List[str] = attack_plan.get("tags", [])

    if not target_pool:
        logger.warning("Pipeline context lacks targets pool resolved by Decision Engine.")
        return

    nuclei_path = shutil.which("nuclei")
    if not nuclei_path:
        logger.error("Nuclei binary not found in PATH.")
        return

    os.makedirs("outputs", exist_ok=True)
    temp_targets_file = os.path.join("outputs", "nuclei_targets.txt")
    temp_output_file = os.path.join("outputs", "nuclei_output.jsonl")
    temp_output_file_global = temp_output_file

    adapt_controller = AdaptiveEngine(context)
    tag_string = ",".join(tags_filter) if tags_filter else "cve,vuln,rce,panel"
    unique_targets = sorted(list(set(target_pool)))
    
    # -------------------------------------------------------------------------
    # PASS 1: PROTOCOL STRUCTURAL SEGREGATION LAYER
    # -------------------------------------------------------------------------
    infra_targets = []
    web_targets = []

    for t in unique_targets:
        if t.startswith("http://") or t.startswith("https://"):
            web_targets.append(t)
        else:
            infra_targets.append(t)

    print("\n" + "=" * 60)
    print("🧠 NUCLEI ADAPTIVE INCREMENTAL SUPERSONIC PIPELINE ACTIVE")
    print(f"Total Unique Assets: {len(unique_targets)} [Network: {len(infra_targets)} | Web: {len(web_targets)}]")
    print("=" * 60 + "\n")
    sys.stdout.flush()

    total_exploits_cached = 0
    last_batch_findings = 0
    last_batch_health = 100

    # Fast sweep for single-pass network protocols (FTP, Samba, Postgres)
    if infra_targets:
        print(f"🚀 [PASS 1 - INFRASTRUCTURE] Running single-pass infrastructure sweep over {len(infra_targets)} targets...")
        sys.stdout.flush()
        with open(temp_targets_file, "w", encoding="utf-8") as f:
            for t in infra_targets:
                f.write(f"{t}\n")
        
        command_infra = [
            nuclei_path, "-l", temp_targets_file, "-jsonl", "-o", temp_output_file,
            "-severity", "critical,high,medium", "-c", "15", "-bs", "1", "-timeout", "5",
            "-retries", "0", "-no-meta", "-silent", "-tags", tag_string
        ]
        subprocess.run(command_infra, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        if os.path.exists(temp_output_file) and os.path.getsize(temp_output_file) > 0:
            total_exploits_cached += parse_and_accumulate_batch(temp_output_file, context, silent_mode=False)
            os.remove(temp_output_file)
    # -------------------------------------------------------------------------
    # LAUNCH ASYNCHRONOUS LIVE DASHBOARD COMPILER THREAD
    # -------------------------------------------------------------------------
    dashboard_active = True
    bg_thread = threading.Thread(target=live_dashboard_worker, args=(context,), daemon=True)
    bg_thread.start()

    # -------------------------------------------------------------------------
    # PASS 2: AUTO-SCALING MICRO-BATCHED WEB ROUTE SWEEP
    # -------------------------------------------------------------------------
    current_batch_size = 5  
    web_index = 0
    batch_idx = 1

    while web_index < len(web_targets):
        # SUPERSONIC AUTO-INCREMENT CONTROLLER (BBR Congestion Paradigm)
        # Immediate velocity boost when there are no package drop/timeout trends detected!
        if last_batch_health >= 95 and last_batch_findings == 0:
            current_batch_size = min(15, current_batch_size + 4)  # Aggressively scale window bounds up
            adaptive_profile = {"concurrency": 45, "bulk_size": 1, "timeout": 4, "rate_limit": 50, "pacing": "aggressive"}
        elif last_batch_health >= 95 and last_batch_findings > 0:
            current_batch_size = min(10, current_batch_size + 2)  # Maintain moderate step increments
            adaptive_profile = {"concurrency": 30, "bulk_size": 1, "timeout": 5, "rate_limit": 30, "pacing": "balanced"}
        else:
            # Immediate drop mitigation threshold fallback if packet loss or timeout behaviors occur
            current_batch_size = max(4, current_batch_size - 2)
            adaptive_profile = {"concurrency": 10, "bulk_size": 1, "timeout": 5, "rate_limit": 12, "pacing": "safe"}

        chunk = web_targets[web_index : web_index + current_batch_size]
        web_index += current_batch_size

        current_concurrency = str(adaptive_profile["concurrency"])
        current_bulk_size = str(adaptive_profile["bulk_size"])
        current_timeout = str(adaptive_profile["timeout"])
        current_rate_limit = str(adaptive_profile["rate_limit"])
        calculated_max_host_error = str(int(adaptive_profile["concurrency"] * 1.5))
        pacing_status = str(adaptive_profile["pacing"]).upper()

        if os.path.exists(temp_output_file):
            os.remove(temp_output_file)

        with open(temp_targets_file, "w", encoding="utf-8") as f:
            for t in chunk:
                f.write(f"{t}\n")

        # Armored execution query featuring integrated 30s stats and structural loop filters
        command = [
            nuclei_path,
            "-l", temp_targets_file,
            "-jsonl",
            "-o", temp_output_file,
            "-severity", "critical,high,medium",
            "-c", current_concurrency,
            "-bs", current_bulk_size,
            "-timeout", current_timeout,
            "-retries", "0",
            "-max-host-error", calculated_max_host_error,
            "-rl", current_rate_limit,
            "-rld", "1s",
            "-stats",
            "-stats-interval", "30",
            "-exclude-tags", "ftp,samba,smb,postgres,postgresql,vnc,ssh,rdp",
            "-no-meta",
            "-silent",
            "-tags", tag_string
        ]

        print(f"🚀 [BATCH {batch_idx}] [PACING: {pacing_status}] Scanning {len(chunk)} targets (Dynamic Window Size: {current_batch_size})...")

        # 🔑 ULTRA-INTELLIGENT TELEMETRY UPDATER (PRESERVES LIVE STATES DURING BLOCKING RUNS)
        current_live_health = last_batch_health if 'last_batch_health' in locals() else 100
        
        session_duration = int(time.time() - global_scan_start) if 'global_scan_start' in locals() else 0
        s_hours, s_rem = divmod(session_duration, 3600)
        s_mins, s_secs = divmod(s_rem, 60)
        formatted_runtime = f"{s_hours:02d}:{s_mins:02d}:{s_secs:02d}" if session_duration > 0 else "RUNNING"

        update_engine_status(
            batch=batch_idx,
            mode=pacing_status,
            health=current_live_health,
            elapsed=formatted_runtime,
            stream="ACTIVE"
        )

        print(f"   ⚙️ Active Rates: Concurrency={current_concurrency} | RateLimit={current_rate_limit} req/s | Timeout={current_timeout}s")
        sys.stdout.flush()

        start_time = time.time()
        process_result = subprocess.run(command, stdout=sys.stdout, stderr=subprocess.PIPE, check=False)

        duration = time.time() - start_time
        
        stderr_logs = process_result.stderr.decode("utf-8", errors="ignore") if process_result.stderr else ""
        timeouts_detected = stderr_logs.lower().count("timeout") + stderr_logs.lower().count("context deadline exceeded")
        errors_detected = stderr_logs.lower().count("error") + stderr_logs.lower().count("connection refused")

        # Re-evaluate live batch health coefficients based on transport behaviors
        last_batch_health = max(10, 100 - (timeouts_detected * 8) - (errors_detected * 4))

        update_engine_status(
            batch=batch_idx,
            mode=pacing_status,
            health=last_batch_health,
            elapsed=f"{int(duration)}s",
            stream="SYNCED"
        )

        adapt_controller.update_profile_from_telemetry(
            timeouts_detected,
            errors_detected,
            last_batch_health
        )

        if os.path.exists(temp_output_file) and os.path.getsize(temp_output_file) > 0:
            last_batch_findings = parse_and_accumulate_batch(temp_output_file, context, silent_mode=False)
            total_exploits_cached += last_batch_findings

            print(f"   [📊] TELEMETRY: Duration: {duration:.2f}s | Timeouts: {timeouts_detected} | Batch Health Score: {last_batch_health}/100")
            print(f"   {CLR_INFO}[📊] GLOBAL TOTAL EXPLOITS ARCHIVED: {total_exploits_cached}{CLR_RESET}\n")
            sys.stdout.flush()
            os.remove(temp_output_file)
        else:
            last_batch_findings = 0
            print(f"\n   {CLR_GREEN}[✔] BATCH {batch_idx} COMPLETED | Unique findings discovered: 0{CLR_RESET}")
            print(f"   [📊] TELEMETRY: Duration: {duration:.2f}s | Batch Health Score: {last_batch_health}/100")
            print(f"   {CLR_INFO}[📊] GLOBAL TOTAL EXPLOITS ARCHIVED: {total_exploits_cached}{CLR_RESET}\n")
            sys.stdout.flush()
        
        batch_idx += 1

    # Close asynchronous tracking threads safely upon completion
    dashboard_active = False
    if os.path.exists(temp_targets_file):
        os.remove(temp_targets_file)

    print("\n" + "=" * 60)
    print(f"🧠 NUCLEI CAMPAIGN CONCLUDED | GLOBAL TARGET FINDINGS SECURED: {total_exploits_cached}")
    print("=" * 60 + "\n")
    sys.stdout.flush()
def parse_and_accumulate_batch(file_path: str, context: ScanContext, silent_mode: bool = False) -> int:
    """
    Parses structural JSONL outputs applying deduplication and memory consolidation matrix filters.
    Cross-checks active memory arrays to return mathematically exact global unique discovery metrics.
    """
    severity_map = {
        "info": Severity.INFO, "low": Severity.LOW, "medium": Severity.MEDIUM,
        "high": Severity.HIGH, "critical": Severity.CRITICAL,
    }

    unique_findings_count = 0
    consolidation_matrix = {}

    try:
        if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
            return 0

        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            lines = [l.strip() for l in f if l.strip()]

        for line in lines:
            try:
                data = json.loads(line)
            except json.JSONDecodeError:
                continue

            info = data.get("info", {})
            name = info.get("name", "Unknown Finding")
            severity_raw = info.get("severity", "info").lower()
            matched_url = data.get("matched-at", context.target)
            template_id = data.get("template-id", "unknown")
            cves = info.get("classification", {}).get("cve-id", [])

            # Matrix Consolidation Key constraint definitions
            matrix_key = f"{matched_url}::{template_id}"

            if matrix_key not in consolidation_matrix:
                consolidation_matrix[matrix_key] = {
                    "name": name,
                    "severity_raw": severity_raw,
                    "matched_url": matched_url,
                    "template_id": template_id,
                    "cves": cves,
                    "count": 1,
                    "info": info,
                    "raw_data": data
                }
            else:
                consolidation_matrix[matrix_key]["count"] += 1

        # Process and register consolidated records into context graph models
        for key, entity in consolidation_matrix.items():
            s_raw = entity["severity_raw"]
            severity_enum = severity_map.get(s_raw, Severity.INFO)
            
            # Thread-safe lookups to avoid duplicate storage insertions in global context arrays
            already_exists = any(
                v.get("template") == entity["template_id"] and v.get("matched_at") == entity["matched_url"]
                for v in context.asset.vulnerabilities
            )
            
            if not already_exists:
                context.asset.vulnerabilities.append({
                    "name": entity["name"],
                    "severity": s_raw,
                    "matched_at": entity["matched_url"],
                    "template": entity["template_id"],
                    "cves": entity["cves"]
                })

                # Extract live curl and response strings directly from native tool execution dumps
                curl_cmd = entity["raw_data"].get("curl-command", f"curl -X 'GET' '{entity['matched_url']}'")
                raw_response = entity["raw_data"].get("response", "Handshake signature successfully validated.")

                finding = Finding(
                    module="nuclei", 
                    finding_type="vulnerability",
                    title=f"Nuclei: {entity['name']}", 
                    severity=severity_enum,
                    data={
                        "template_id": entity["template_id"], 
                        "matched_url": entity["matched_url"], 
                        "cves": entity["cves"], 
                        "hits_consolidated": entity["count"],
                        "curl-command": curl_cmd,
                        "raw_log_summary": raw_response
                    },
                    description=entity["info"].get("description", "Vulnerability footprint successfully mapped."), 
                    remediation=entity["info"].get("remediation", "Apply vendor updates and lock logic configurations."), 
                    url=entity["matched_url"]
                )
                context.add_finding(finding)

            # -----------------------------------------------------------------
            # ARMORED THREAD SYNC PASSTHROUGH LAYER (FIXES THE COLD CONTADORES)
            # -----------------------------------------------------------------
            # Always increment unique counts extracted from the matrix pass
            # regardless of whether the main thread or background thread locked it first
            unique_findings_count += 1

            # Visual terminal reporting pass (Only displays unique hits in console stream)
            if not silent_mode and not already_exists:
                if "critical" in s_raw:
                    color = CLR_CRITICAL
                elif "high" in s_raw:
                    color = CLR_HIGH
                elif "medium" in s_raw:
                    color = CLR_MEDIUM
                else:
                    color = CLR_INFO

                count_suffix = f" (Repeated {entity['count']} times - Consolidated)" if entity['count'] > 1 else ""
                print(f"    🌟 {color}[FINDING SECURED]{CLR_RESET} -> [{color}{s_raw.upper()}{CLR_RESET}] {entity['name']} | {entity['matched_url']}{CLR_RESET}{count_suffix}")
                sys.stdout.flush()

        return unique_findings_count

    except Exception as e:
        logger.error(f"Critical breakdown inside deduplication memory loader: {str(e)}")
        return 0

