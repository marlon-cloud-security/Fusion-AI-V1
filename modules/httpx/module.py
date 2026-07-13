# modules/httpx/module.py

import logging
import requests
import urllib3
from core.types import ScanContext, Finding, Severity

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logger = logging.getLogger("FusionEngine.Modules.Httpx")

session = requests.Session()
session.headers.update({
    "User-Agent": "FusionAI-ProbingEngine/1.0"
})

def run(context: ScanContext) -> None:
    """
    HTTPX Probing Layer (adaptive L7 validation).
    Detects real HTTP services based on response behavior and populates the central Asset model.
    """
    if not context.open_ports:
        logger.warning("No open ports available for HTTP probing.")
        return

    logger.info(f"Probing {len(context.open_ports)} ports for HTTP behavior detection...")

    timeout = 2.5
    probes = []

    for port in context.open_ports:
        candidates = [
            f"http://{context.target}:{port}",
            f"https://{context.target}:{port}"
        ]

        for url in candidates:
            try:
                response = session.get(
                    url,
                    timeout=timeout,
                    verify=False,
                    allow_redirects=True
                )

                status = response.status_code
                content_type = response.headers.get("Content-Type", "")

                if status < 200 or status >= 600:
                    continue

                looks_like_web = (
                    "html" in content_type.lower()
                    or "text" in content_type.lower()
                    or "json" in content_type.lower()
                    or "xml" in content_type.lower()
                )

                if not looks_like_web:
                    continue

                server = response.headers.get("Server", "unknown")

                # 1. FEED THE ASSET DIRECTLY (Structured Knowledge Mapping)
                context.asset.web_servers.append({
                    "url": url,
                    "port": port,
                    "status_code": status,
                    "server_banner": server
                })

                context.web_targets.append(url)
                probes.append(url)

                severity = Severity.INFO
                if port not in {80, 443}:
                    severity = Severity.MEDIUM

                # 2. Generate finding evidence passing the target parameters
                finding = Finding(
                    module="httpx",
                    finding_type="web_service",
                    title=f"HTTP Service Detected: {url}",
                    severity=severity,
                    data={
                        "url": url,
                        "port": port,
                        "status_code": status,
                        "server": server
                    },
                    description=f"Valid HTTP response detected at {url} with status {status}",
                    remediation="Limit exposure of web services and harden server headers.",
                    port=port,
                    url=url
                )

                context.add_finding(finding)
                logger.info(f"HTTP detected -> {url} [{status}]")
                break  

            except requests.exceptions.RequestException:
                continue

    logger.info(f"HTTPX scan complete | Active web targets populated into AssetHost: {len(probes)}")
