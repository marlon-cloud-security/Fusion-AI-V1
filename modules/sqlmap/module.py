# modules/sqlmap/module.py

import logging
import subprocess
import shutil
import os
import sys
from urllib.parse import urlparse, parse_qs
from core.types import ScanContext, Finding, Severity
from intelligence.adaptive_engine import AdaptiveEngine

logger = logging.getLogger("FusionEngine.Modules.Sqlmap")

def run(context: ScanContext) -> None:
    """
    Executes a fully automated, context-aware adaptive SQLMap injection campaign.
    Eliminates human prompts for unattended cloud orchestration, performs parameter-based
    vulnerability prioritizing, and utilizes adaptive profiling to throttle injection rates.
    """
    if not context.vulnerable_urls:
        logger.warning("Pipeline context lacks parameter-based URLs. Skipping Sqlmap exploitation step.")
        return

    sqlmap_path = shutil.which("sqlmap")
    if not sqlmap_path:
        logger.error("Sqlmap binary missing from system PATH. Skipping execution workflow.")
        return

    # -------------------------------------------------------------------------
    # LAYER 1: HEURISTIC PARAMETER PRIORITIZATION ENGINE
    # -------------------------------------------------------------------------
    # Premium products don't just slice list slices randomly. They rank high-risk entrypoints.
    unique_urls = list(set(context.vulnerable_urls))
    high_risk_endpoints = []
    baseline_endpoints = []

    # High-impact SQL injection patterns common in vulnerable web applications
    db_keywords = ["id", "select", "page", "query", "search", "user", "cat", "item", "file", "view"]

    for url in unique_urls:
        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        if not params:
            continue  # Drop URLs lacking explicit parameters to protect server bandwidth

        # Categorize targets based on key token occurrences
        has_risk_token = any(keyword in str(params.keys()).lower() for keyword in db_keywords)
        if has_risk_token:
            high_risk_endpoints.append(url)
        else:
            baseline_endpoints.append(url)

    # Consolidate ordered execution vector queue
    prioritized_targets = high_risk_endpoints + baseline_endpoints
    total_found = len(prioritized_targets)

    if total_found == 0:
        logger.warning("No structural parameters identified in context query strings. Skipping Sqlmap.")
        return

    # -------------------------------------------------------------------------
    # LAYER 2: CLOSED-LOOP ADAPTIVE BOUNDS CALCULATION
    # -------------------------------------------------------------------------
    # Fetches active pacing metrics calculated from previous Nuclei milestones
    adapt_controller = AdaptiveEngine(context)
    adaptive_profile = adapt_controller.calculate_adaptive_profile()
    pacing_status = str(adaptive_profile.get("pacing", "balanced")).lower()

    # Automatically set exploit limits and performance threads based on server health matrix
    if pacing_status == "aggressive":
        sample_limit = min(30, total_found)
        sqlmap_threads = "4"
        performance_flags = ["--keep-alive", "--null-connection"]
    elif pacing_status == "balanced":
        sample_limit = min(15, total_found)
        sqlmap_threads = "2"
        performance_flags = ["--keep-alive"]
    else:
        sample_limit = min(5, total_found) # Protective fallback for legacy or low-RAM environments
        sqlmap_threads = "1"
        performance_flags = []



    print("\n🎯 SQLMAP VECTOR CONTROL")
    print(f"Available exploit vectors: {len(prioritized_targets)}")
    print("Enter number to test (0 = ALL):")

    try:
        user_limit = int(input("SQLMAP LIMIT > "))

        if user_limit == 0:
            sample_limit = len(prioritized_targets)
        else:
            sample_limit = min(user_limit, len(prioritized_targets))

    except ValueError:
        print("Invalid input. Using adaptive default.")


    target_endpoints = prioritized_targets[:sample_limit]


    print("\n" + "=" * 60)
    print("🎯 FUSION-AI AUTOMATED SQL INJECTION SUB-SYSTEM ACTIVE")
    print(f"Total Discovered Entrypoints: {total_found} | Ranked High-Risk Targets Mapped: {len(high_risk_endpoints)}")
    print(f"Adaptive Target Allocation Committed: Evaluating {len(target_endpoints)} vectors using Thread-Cap={sqlmap_threads}")
    print("=" * 60 + "\n")
    sys.stdout.flush()

    output_directory = "outputs/sqlmap_out"

    # -------------------------------------------------------------------------
    # LAYER 3: ADAPTIVE INJECTION LOOP EXECUTION
    # -------------------------------------------------------------------------
    for idx, url in enumerate(target_endpoints):
        # Base automated command setup with performance optimization parameters
        command = [
            sqlmap_path, 
            "-u", url, 
            "--batch",              # Enforces fully automated interactions without human prompt freezes
            "--random-agent",       # Spoofs real-world user agent strings
            "--flush-session",      # Erases cache residue to ensure fresh network injection analysis
            "--output-dir", output_directory,
            f"--threads={sqlmap_threads}",
            "--tech=BEUSTQ",        # Scans comprehensively: Boolean, Error, Union, Stacked, Time, Q-Injections
            "--level=1"
        ] + performance_flags
        
        try:
            print("\n" + "=" * 50)
            print(f" 🔥 LAUNCHING LIVE EXPLOIT VECTOR [{idx + 1}/{len(target_endpoints)}] OVER: {url}")
            print("=" * 50 + "\n")
            sys.stdout.flush()

            # Execute automated binary mapping with runtime stdout terminal streaming inheritance
            subprocess.run(command, stdout=sys.stdout, stderr=sys.stderr, timeout=180.0, check=False)
            parse_sqlmap_results(output_directory, context, url)

        except subprocess.TimeoutExpired:
            logger.warning(f"Injection threshold ceiling reached (Timeout) over vector: {url}. Moving forward.")
            continue
        except Exception as e:
            logger.error(f"Unexpected operational crash inside Sqlmap orchestrator loop: {str(e)}")
            continue

    # -------------------------------------------------------------------------
    # LAYER 4: WORKFLOW SUMMARY TELEMETRY (EXECUTIVE SUITE REPORTING)
    # -------------------------------------------------------------------------
    sqlmap_breaches = [v for v in context.asset.vulnerabilities if v.get("template_id") == "sqlmap_injection"]
    confirmed_count = len(sqlmap_breaches)

    print("\n" + "=" * 60)
    print(" 🏁 AUTOMATED SQLMAP EXPLOITATION SEQUENCE CONCLUDED")
    print(f" Total Mapped Parameter Channels Evaluated: {len(target_endpoints)}")
    print(f" Confirmed Backend Database Penetrations: {confirmed_count}")
    
    if confirmed_count > 0:
        print("\n [!] CRITICAL UNDERLYING DATABASE EMBEDDED BREACHES CONFIRMED:")
        for breach in sqlmap_breaches:
            print(f"  -> TARGET COMPROMISED: {breach['matched_at']}")
    else:
        print("\n [*] Status: No query parameters were successfully broken using injection techniques.")
    print("=" * 60 + "\n")
    sys.stdout.flush()

    logger.info(f"Sqlmap stage processing completed | Operational injections logged: {confirmed_count}")


def parse_sqlmap_results(output_dir: str, context: ScanContext, target_url: str) -> None:
    """
    Inspects structural text file logging outputs to parse and aggregate active SQL Injection 
    breaches directly into the central context vulnerabilities graph model.
    """
    if not os.path.exists(output_dir):
        return

    for root, dirs, files in os.walk(output_dir):
        if "log" in files:
            log_file_path = os.path.join(root, "log")
            try:
                with open(log_file_path, "r", encoding="utf-8", errors="replace") as file:
                    log_content = file.read()
                    
                if "parameter" in log_content.lower() or "type:" in log_content.lower():
                    # Central context structure reporting update mapping
                    context.asset.vulnerabilities.append({
                        "name": "SQL Injection Matrix Breach",
                        "severity": "critical", 
                        "cves": [], 
                        "template_id": "sqlmap_injection", 
                        "matched_at": target_url
                    })

                    # Generate high-utility structured item report entries
                    finding = Finding(
                        module="sqlmap", 
                        finding_type="sql_injection",
                        title=f"Critical SQL Injection Vulnerability: {target_url}", 
                        severity=Severity.CRITICAL,
                        data={"matched_url": target_url, "raw_log_summary": log_content[:500]},
                        description="Database manipulation token discovered. Attackers can execute drop operations or dump full schema fields.",
                        remediation="Implement strict parameterized query layers, leverage enterprise secure ORM components, and enable strict type casting whitelist validation models.", 
                        url=target_url
                    )
                    context.add_finding(finding)
                    logger.info(f"CRITICAL BREACH IDENTIFIED -> SQL Injection confirmed at {target_url}")
            except Exception as e:
                logger.error(f"Failed to read Sqlmap telemetry storage files: {str(e)}")


