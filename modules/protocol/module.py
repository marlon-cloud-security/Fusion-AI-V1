# modules/protocol/module.py

import logging
from core.types import ScanContext, Finding, Severity

logger = logging.getLogger("FusionEngine.Modules.ProtocolHeuristic")

# Services that often hide HTTP behind non-standard ports
WEB_LIKE_SERVICES = {
    80, 443, 8000, 8080, 8443,
    3000, 5000, 8008, 8081,
    8888, 9000, 10000, 50000,
    7001, 7002, 7003, 7004, 7005, 7006
}

def run(context: ScanContext) -> None:
    """
    Infers potential web services from raw port scan results.
    This is NOT HTTP probing. This is intelligent classification.
    """
    if not context.open_ports:
        return

    logger.info("Running protocol heuristic classification layer...")

    for port in context.open_ports:
        # Weak signal detection (do NOT assume HTTP)
        if port in WEB_LIKE_SERVICES:
            finding = Finding(
                module="protocol_heuristic",
                finding_type="service_inference",
                title=f"Potential Web Interface Candidate: Port {port}",
                severity=Severity.INFO,
                data={
                    "port": port,
                    "confidence": "medium"
                },
                description=(
                    "Port matches common web infrastructure patterns. "
                    "Requires HTTPX validation."
                ),
                remediation="Validate with HTTP probing layer before classification."
            )

            context.add_finding(finding)
            logger.debug(f"Web candidate inferred on port {port}")

    logger.info("Protocol heuristic analysis completed")
