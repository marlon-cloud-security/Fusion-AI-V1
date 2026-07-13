# modules/whatweb/module.py

import logging
import requests
import re
import urllib3
from core.types import ScanContext, Finding, Severity

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logger = logging.getLogger("FusionEngine.Modules.WhatWeb")

def run(context: ScanContext) -> None:
    """
    Executes advanced web technology fingerprinting over verified web targets.
    Maps software footprints directly to the universal Asset technologies matrix.
    """
    if not context.web_targets:
        logger.warning("Pipeline context lacks active web targets. Skipping WhatWeb fingerprinting.")
        return

    logger.info(f"Analyzing {len(context.web_targets)} web targets for technology fingerprinting...")

    signatures = {
        "Apache": r"Apache/?([\d\.]+)?",
        "Nginx": r"nginx/?([\d\.]+)?",
        "PHP": r"PHP/?([\d\.]+)?",
        "WordPress": r"wp-content|wordpress",
        "Ubuntu": r"Ubuntu",
        "Debian": r"Debian",
        "Twiki": r"twiki",
        "PhpMyAdmin": r"phpmyadmin"
    }

    session = requests.Session()
    session.headers.update({"User-Agent": "Fusion-AI/1.0-FingerprintEngine"})
    
    for url in context.web_targets:
        try:
            logger.debug(f"Fingerprinting application stack components at: {url}")
            response = session.get(url, timeout=3.0, verify=False, allow_redirects=True)
            
            server_header = response.headers.get("Server", "")
            x_powered_by = response.headers.get("X-Powered-By", "")
            html_body = response.text
            
            detected_techs = []
            metadata_payload = {}

            if server_header:
                detected_techs.append(f"Server Source: {server_header}")
                metadata_payload["raw_server"] = server_header

            if x_powered_by:
                detected_techs.append(f"Runtime Language: {x_powered_by}")
                metadata_payload["runtime"] = x_powered_by

            for tech_name, pattern in signatures.items():
                if re.search(pattern, html_body, re.IGNORECASE) or re.search(pattern, server_header, re.IGNORECASE):
                    match = re.search(pattern, server_header if tech_name in ["Apache", "Nginx"] else html_body, re.IGNORECASE)
                    version = match.group(1) if match and match.lastindex else "Version Unknown"
                    
                    # 1. FEED THE ASSET TECHNOLOGIES RECORD DIRECTLY
                    tech_string = f"{tech_name}:{version}"
                    if tech_string not in context.asset.technologies:
                        context.asset.technologies.append(tech_string)
                    
                    detected_techs.append(f"{tech_name} ({version})")
                    metadata_payload[tech_name.lower()] = version

            if detected_techs:
                finding = Finding(
                    module="whatweb",
                    finding_type="technology_fingerprint",
                    title=f"Web Technology Stack Discovered: {url}",
                    severity=Severity.INFO,
                    data={
                        "url": url,
                        "components": detected_techs,
                        "raw_metadata": metadata_payload
                    },
                    description=f"Passive signature mapping identified the following deployment stack: {', '.join(detected_techs)}",
                    remediation="Minimize descriptive signature footprints. Disable X-Powered-By headers and mask server banners.",
                    url=url
                )
                context.add_finding(finding)
                logger.info(f"Fingerprint layout finalized for {url} -> Stack: {detected_techs}")

        except requests.exceptions.RequestException as e:
            logger.debug(f"Failed to complete fingerprint handshake execution on {url}: {str(e)}")
            continue

    logger.info(f"WhatWeb fingerprint stage complete | Asset technologies populated: {len(context.asset.technologies)}")
