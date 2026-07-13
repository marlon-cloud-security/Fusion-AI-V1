
















# modules/ffuf/module.py

import logging
import subprocess
import shutil
import os
import json
import sys
from urllib.parse import urlparse
from core.types import ScanContext, Finding, Severity

logger = logging.getLogger("FusionEngine.Modules.Ffuf")

def run(context: ScanContext) -> None:
    """
    Executes a high-speed web fuzzing campaign using native Ffuf.
    Streams output live to the terminal with its native progress layout 
    while storing results in a JSON cache for background ingestion.
    """
    if not context.web_targets:
        logger.warning("Pipeline context lacks active web targets. Skipping Ffuf fuzzing.")
        return

    ffuf_path = shutil.which("ffuf")
    if not ffuf_path:
        logger.error("Ffuf binary missing from system PATH. Skipping web fuzzing layer.")
        return

    # Utilizing standard wordlist allocation inside Kali Linux
    wordlist_path = "/usr/share/wordlists/dirb/common.txt"
    if not os.path.exists(wordlist_path):
        logger.error(f"Ffuf target wordlist missing: '{wordlist_path}'.")
        return

    logger.info(f"Triggering high-speed web fuzzing [Ffuf] over {len(context.web_targets)} targets...")

    for url in context.web_targets:
        # Enforcing clear absolute URL mapping for Ffuf syntax injection (requires FUZZ keyword)
        fuzz_target_url = f"{url.rstrip('/')}/FUZZ"
        temp_output_json = "outputs/ffuf_temp.json"

        # FIXED DUAL STREAM: We REMOVE the "-s" (silent) flag so Ffuf renders its live progress bar.
        # -mc 200,301,302 filters down exclusively to successful handshake pathways.
        command = [
            ffuf_path,
            "-u", fuzz_target_url,
            "-w", wordlist_path,
            "-mc", "200,301,302",
            "-o", temp_output_json,
            "-of", "json"
        ]
        
        try:
            print("\n" + "="*50)
            print(f" 🔥 LAUNCHING HIGH-SPEED FFUF STREAM OVER: {url}")
            print("="*50 + "\n")
            sys.stdout.flush()

            # By removing capture_output and connecting to sys.stdout, the binary inherits 
            # your actual terminal screen, displaying its beautiful layout and statistics live.
            subprocess.run(command, stdout=sys.stdout, stderr=sys.stderr, timeout=120.0, check=False)

            print("\n" + "="*50)
            print(" 🧠 FFUF STREAM FINALIZED. INGESTING PATHWAYS INTO ASSET...")
            print("="*50 + "\n")
            sys.stdout.flush()
            
            if os.path.exists(temp_output_json) and os.path.getsize(temp_output_json) > 0:
                parse_ffuf_json(temp_output_json, context, url)
                os.remove(temp_output_json)

        except Exception as e:
            logger.error(f"Unexpected operational crash inside Ffuf fuzzing loop: {str(e)}")
            if os.path.exists(temp_output_json):
                os.remove(temp_output_json)
            continue

def parse_ffuf_json(file_path: str, context: ScanContext, base_url: str) -> None:
    """
    Parses structural JSON outputs from Ffuf and converts hits into normalized Findings and Assets.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            
        results = data.get("results", [])
        if not results:
            return

        discovered_endpoints = []

        for item in results:
            input_path = item.get("input", {}).get("FUZZ", "")
            status_code = item.get("status", 0)
            
            full_hit_url = f"{base_url.rstrip('/')}/{input_path}"
            discovered_endpoints.append(f"/{input_path} (Status: {status_code})")
            
            # 1. FEED THE ASSET DIRECTORIES MATRIX (Knowledge Graph)
            parsed_hit = urlparse(full_hit_url)
            if parsed_hit.path and parsed_hit.path not in context.asset.directories:
                context.asset.directories.append(parsed_hit.path)

            # 2. Feed the downstream injection pipeline with newly unmasked parameter sets
            if any(ext in input_path for ext in [".php", ".html", ".jsp"]):
                if "?" in full_hit_url or "=" in full_hit_url:
                    context.vulnerable_urls.append(full_hit_url)

        if discovered_endpoints:
            # Wrap telemetry items directly into our standard finding contract as evidence
            finding = Finding(
                module="ffuf", 
                finding_type="web_fuzzing",
                title=f"Sensitive Web Pathways Fuzzed: {base_url}",
                severity=Severity.HIGH if any("config" in path or "admin" in path for path in discovered_endpoints) else Severity.MEDIUM,
                data={
                    "base_url": base_url,
                    "total_fuzz_hits": len(discovered_endpoints),
                    "hits_summary": discovered_endpoints
                },
                description=f"High-speed fuzzing successfully uncovered {len(discovered_endpoints)} unlinked server routes.",
                remediation="Remove sensitive development backups, restrict public access to hidden endpoints, and enforce strict 403 authorization routing.",
                url=base_url
            )
            context.add_finding(finding)
            logger.info(f"Ffuf background ingestion complete | Asset directories size: {len(context.asset.directories)}")

    except Exception as e:
        logger.error(f"Failed to process or parse Ffuf log data structure: {str(e)}")




















