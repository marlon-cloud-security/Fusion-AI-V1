# modules/katana/module.py

import logging
import subprocess
import shutil
import os
import sys
from urllib.parse import urlparse
from core.types import ScanContext, Finding, Severity

logger = logging.getLogger("FusionEngine.Modules.Katana")

def run(context: ScanContext) -> None:
    """
    Executes a real native Katana crawler binary using subprocess.
    Streams execution live to stdout and harvests hundreds of parameters for Sqlmap feeding.
    """
    if not context.web_targets:
        logger.warning("No web targets available for Katana crawling. Skipping step.")
        return

    katana_path = shutil.which("katana")
    if not katana_path:
        logger.error("Katana Go binary missing from system PATH.")
        return

    logger.info("Initializing high-performance native Katana crawler thread...")
    temp_crawl_txt = "outputs/katana_temp.txt"

    for url in context.web_targets:
        # FIXED: Reordered flags to prevent syntax injection collisions.
        # -jc (Crawl Javascript), -kf all (Extract all known endpoints fields)
        command = [
            katana_path, 
            "-u", url, 
            "-o", temp_crawl_txt, 
            "-jc", 
            "-kf", "all"
        ]
        
        try:
            print("\n" + "="*50)
            print(f" 🕷️  LAUNCHING NATIVE KATANA GO SPIDER OVER: {url}")
            print("="*50 + "\n")
            sys.stdout.flush()

            # The Go binary inherits your terminal screen, displaying live crawling progress bars!
            subprocess.run(command, stdout=sys.stdout, stderr=sys.stderr, timeout=180.0, check=False)

            print("\n" + "="*50)
            print(" 🧠 KATANA SPIDER SEQUENCE FINALIZED. PARSING HARVESTED ENDPOINTS...")
            print("="*50 + "\n")
            sys.stdout.flush()

            if os.path.exists(temp_crawl_txt) and os.path.getsize(temp_crawl_txt) > 0:
                parse_katana_output(temp_crawl_txt, context, url)
                os.remove(temp_crawl_txt)
            else:
                logger.warning(f"Katana raw stream finished for {url} with no files stored.")

        except Exception as e:
            logger.error(f"Fatal operational crash inside Katana binary orchestrator thread: {str(e)}")
            if os.path.exists(temp_crawl_txt):
                os.remove(temp_crawl_txt)
            continue

def parse_katana_output(file_path: str, context: ScanContext, base_url: str) -> None:
    """Ingests raw line-by-line Katana text outputs to build asset directory models."""
    try:
        discovered_links_count = 0
        parameter_urls = []
        parsed_base = urlparse(base_url)

        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                link = line.strip()
                if not link:
                    continue

                parsed_absolute = urlparse(link)
                if parsed_absolute.netloc != parsed_base.netloc:
                    continue

                discovered_links_count += 1
                
                clean_path = parsed_absolute.path if parsed_absolute.path else "/"
                if clean_path not in context.asset.directories:
                    context.asset.directories.append(clean_path)

                if parsed_absolute.query or "=" in link:
                    parameter_urls.append(link)

        if parameter_urls:
            context.vulnerable_urls.extend(parameter_urls)
            logger.info(f"Katana successfully isolated {len(parameter_urls)} high-risk parameters for SQLMap validation.")

        finding = Finding(
            module="katana", finding_type="web_crawling",
            title=f"Application Directory Map: {base_url}", severity=Severity.INFO,
            data={"base_url": base_url, "total_links_discovered": discovered_links_count, "parameter_paths_isolated": len(parameter_urls)},
            description=f"Katana indexed {discovered_links_count} structural assets inside target scope.",
            remediation="Review exposed application endpoint pathways and restrict debug parameters.", url=base_url
        )
        context.add_finding(finding)
        logger.info(f"Katana parsing finalized. Total Asset directories mapped: {len(context.asset.directories)}")

    except Exception as e:
        logger.error(f"Failed to ingest raw Katana log file: {str(e)}")
